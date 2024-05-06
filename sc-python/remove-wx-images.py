import sys
from sshUtils import SSHUtils

IMAGE_DIR = "sat-images/baugh-org.wx/"
sshu = SSHUtils()

# Get the base of the file name from command line arguments
filebase = sys.argv[1]
print(f"Removing files {filebase}* from server...")

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
def remove_file(file_name):
    path_to_delete = IMAGE_DIR + file_name
    try:
        sshu.delete_remote_file(path_to_delete)
        print(f"  successfully removed {file_name}")
    except Exception as err:
        print(err)


# Remove each file
for filename in files:
    remove_file(filename)
