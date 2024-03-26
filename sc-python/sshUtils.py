import paramiko


class SSHUtils:
    def __init__(self, host="www.baugh.org", port=3022, username="pi", password: str = "***REMOVED***"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def upload_file_via_scp(self, local_file_path, remote_file_path):
        try:
            # Create an SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the remote server
            ssh.connect(self.host, self.port, self.username, self.password)

            # Create an SCP client
            scp = ssh.open_sftp()

            # Upload the local file to the remote server
            scp.put(local_file_path, remote_file_path)

            # Close the connection
            scp.close()
            ssh.close()

            print(f"File {local_file_path} uploaded to {self.host}:{remote_file_path} via SCP successfully.")
        except Exception as e:
            print(f"Error uploading file: {str(e)}")


    def upload_file_object_via_scp(self, file_object, remote_file_path):
        # Initialize SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote host
        client.connect(self.host, username=self.username, password=self.password)

        # Upload the array to the remote file
        with client.open_sftp() as sftp:
            sftp.putfo(file_object, remote_file_path)

        # Close the SSH connection
        client.close()

        print(f"Array uploaded to {remote_file_path} on the remote host.")

    def delete_remote_file(self, remote_path):
        try:
            # Create an SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the remote server
            ssh.connect(self.host, self.port, self.username, self.password)

            # Execute the command to delete the file
            command = f"rm {remote_path}"
            stdin, stdout, stderr = ssh.exec_command(command)

            # Check for any errors
            error = stderr.read().decode("utf-8")
            if error:
                print(f"Error deleting file: {error}")
            else:
                print(f"File {remote_path} deleted successfully")

            # Close the SSH connection
            ssh.close()

        except Exception as e:
            print(f"Error: {str(e)}")
