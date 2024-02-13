import boto3
import json
import uuid
from datetime import datetime

# Configure AWS S3
REGION = ""
BUCKET = ""
IMAGE_DIR = "images/"
boto3.setup_default_session(region_name=REGION)
s3 = boto3.client('s3')

def upload_upcoming_passes(filename):
    upcoming_passes_filename = "upcoming_passes.json"
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    count = 0
    all_passes = []
    for line in lines:
        if line.strip():
            fields = line.split(',')
            pass_info = {
                'start': datetime.utcfromtimestamp(int(fields[0])).isoformat(),
                'end': datetime.utcfromtimestamp(int(fields[1])).isoformat(),
                'elevation': fields[2],
                'direction': fields[3],
                'satellite': fields[4],
                'tle1': fields[5],
                'tle2': fields[6].strip()  # Assuming the last field may have a newline character
            }
            all_passes.append(pass_info)
        
        count += 1
        if count == len(lines):
            all_passes.sort(key=lambda x: x['start'])
            print("uploading upcoming pass info")
            params = {
                'ACL': "public-read",
                'ContentType': "application/json",
                'Bucket': BUCKET,
                'Key': IMAGE_DIR + upcoming_passes_filename,
                'Body': json.dumps(all_passes, indent=2)
            }
            try:
                s3.put_object(**params)
                print(f"  successfully uploaded {upcoming_passes_filename}")
            except Exception as e:
                print(e)

# Replace sys.argv[1] with the actual filename if running the script directly
# upload_upcoming_passes(sys.argv[1])

