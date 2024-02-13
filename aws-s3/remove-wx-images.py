import boto3
import sys
import uuid

# Configure AWS S3
REGION = ""
BUCKET = ""
IMAGE_DIR = "images/"
boto3.setup_default_session(region_name=REGION)
s3 = boto3.client('s3')

# Get the base of the file name from command line arguments
filebase = sys.argv[1]
print(f"Removing files {filebase}* from S3...")

# List of files to remove
files = [
    f"{filebase}.json",
    f"{filebase}-ZA.png",
    f"{filebase}-NO.png",
    f"{filebase}-MSA.png",
    f"{filebase}-MSAPRECIP.png",
    f"{filebase}-MCIR.png",
    f"{filebase}-THERM.png",
    f"thumbs/{filebase}-ZA.png",
    f"thumbs/{filebase}-NO.png",
    f"thumbs/{filebase}-MSA.png",
    f"thumbs/{filebase}-MSAPRECIP.png",
    f"thumbs/{filebase}-MCIR.png",
    f"thumbs/{filebase}-THERM.png"
]

# Function to remove a file from S3
def remove_file(filename):
    params = {
        'Bucket': BUCKET,
        'Key': IMAGE_DIR + filename,
    }
    try:
        s3.delete_object(**params)
        print(f"  successfully removed {filename}")
    except Exception as err:
        print(err)

# Remove each file
for filename in files:
    remove_file(filename)

