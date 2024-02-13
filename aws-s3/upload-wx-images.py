import boto3
import os
import glob
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import sys

REGION = ""
BUCKET = ""
LOCATION = ""
IMAGE_DIR = "images/"
boto3.setup_default_session(region_name=REGION)
s3 = boto3.client('s3')

satellite = sys.argv[2]
frequency = sys.argv[3]
filebase = sys.argv[4]
elevation = sys.argv[5]
direction = sys.argv[6]
duration = sys.argv[7]
tle1 = sys.argv[8]
tle2 = sys.argv[9]
gain = sys.argv[10]
chan_a = sys.argv[11]
chan_b = sys.argv[12]
basename = os.path.basename(filebase)
dirname = os.path.dirname(filebase)
components = basename.split("-")
date = components[1]
date = date[:4] + '-' + date[4:6] + '-' + date[6:]
time = components[2]
time = time[:2] + ':' + time[2:4] + ':' + time[4:] + ' ' + datetime.now().strftime("%z")
# example "Gain: 15.2"
if gain:
    gain = gain.split(": ")[1]
# example "Channel A: 1 (visible)"
if chan_a:
    chan_a = chan_a.split(": ")[1]
# example "Channel B: 4 (thermal infrared)"
if chan_b:
    chan_b = chan_b.split(": ")[1]
print(f"Uploading files {basename}* to S3...")
metadata = {
    'satellite': satellite,
    'date': date,
    'time': time,
    'elevation': elevation,
    'direction': direction,
    'duration': duration,
    'imageKey': basename,
    'tle1': tle1,
    'tle2': tle2,
    'frequency': frequency,
    'gain': gain,
    'chan_a': chan_a,
    'chan_b': chan_b,
    'images': []
}

async def upload_image(image, filename):
    w, h = image.size
    enhancement = None
    if filename.endswith("-ZA.png"):
        enhancement = "normal infrared"
    if filename.endswith("-NO.png"):
        enhancement = "color infrared"
    if filename.endswith("-MSA.png"):
        enhancement = "multispectral analysis"
    if filename.endswith("-MSAPRECIP.png"):
        enhancement = "multispectral precip"
    if filename.endswith("-MCIR.png"):
        enhancement = "map color infrared"
    if filename.endswith("-THERM.png"):
        enhancement = "thermal"
    image_info = {
        'filename': filename,
        'width': w,
        'height': h,
        'thumbfilename': 'thumbs/' + filename,
        'enhancement': enhancement
    }
    font = ImageFont.load_default()
    new_image = Image.new('RGB', (w, h + 64), '#000000')
    new_image.paste(image, (0, 48))
    image = new_image
    draw = ImageDraw.Draw(image)
    draw.text((5, 5), f"{metadata['date']} {metadata['time']}  satellite: {metadata['satellite']}  elevation: {metadata['elevation']}°  enhancement: {enhancement}", font=font, fill="#FFFFFF")
    draw.text((5, 25), LOCATION, font=font, fill="#FFFFFF")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    params = {
        'ACL': "public-read",
        'ContentType': "image/png",
        'Bucket': BUCKET,
        'Key': IMAGE_DIR + filename,
        'Body': buffer
    }
    s3.put_object(**params)
    print(f"  successfully uploaded {filename}")
    thumb = image.copy()
    thumb.thumbnail((260, 200))
    thumb_buffer = io.BytesIO()
    thumb.save(thumb_buffer, format="PNG")
    thumb_buffer.seek(0)
    thumb_filename = "thumbs/" + filename
    params = {
        'ACL': "public-read",
        'ContentType': "image/png",
        'Bucket': BUCKET,
        'Key': IMAGE_DIR + thumb_filename,
        'Body': thumb_buffer
    }
    s3.put_object(**params)
    print(f"  successfully uploaded thumb {filename}")
    return image_info

def upload_metadata(filebase):
    metadata_filename = filebase + ".json"
    print(f"uploading metadata {json.dumps(metadata, indent=2)}")
    params = {
        'ACL': "public-read",
        'Bucket': BUCKET,
        'Key': IMAGE_DIR + metadata_filename,
        'Body': json.dumps(metadata, indent=2)
    }
    s3.put_object(**params)
    print(f"  successfully uploaded metadata {metadata_filename}")

files = glob.glob(filebase + "-[A-Z]*.png")
upload_promises = []
for filename in files:
    basename = os.path.basename(filename)
    image = Image.open(filename)
    upload_promises.append(upload_image(image, basename))
    if len(upload_promises) == len(files):
        for future in upload_promises:
            future.result()
        metadata['images'] = [result.result() for result in upload_promises]
        print(f"values: {json.dumps(metadata['images'], indent=2)}")
        upload_metadata(os.path.basename(filebase))


