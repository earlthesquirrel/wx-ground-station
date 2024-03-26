import io
from datetime import datetime
from sshUtils import SSHUtils

sshu = SSHUtils()

# Directory on remote server
IMAGE_DIR = "images/"


def upload_upcoming_passes(filename):
    upcoming_passes_filename = "upcoming_passes.json"
    with open(filename, 'r') as file:
        lines = file.readlines()

    count = 0
    all_passes: list[dict[str, str]] = []
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

            # Convert the array to a string
            all_passes.sort(key=lambda x: x['start'])

            print("uploading upcoming pass info")
            try:
                array_str = "\n".join(str(x) for x in all_passes)
                # Create an in-memory file-like object
                array_file = io.StringIO(array_str)

                sshu.upload_file_object_via_scp(array_file, IMAGE_DIR + upcoming_passes_filename)

                print(f"  successfully uploaded {upcoming_passes_filename}")
            except Exception as e:
                print(e)

# Replace sys.argv[1] with the actual filename if running the script directly
# upload_upcoming_passes(sys.argv[1])
