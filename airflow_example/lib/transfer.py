import paramiko


class SFTPTransferToAnotherSFTP:
    def __init__(
        self,
        source_host,
        source_port,
        source_username,
        source_password,
        destination_host,
        destination_port,
        destination_username,
        destination_password,
    ):
        self.source_host = source_host
        self.source_port = source_port
        self.source_username = source_username
        self.source_password = source_password
        self.destination_host = destination_host
        self.destination_port = destination_port
        self.destination_username = destination_username
        self.destination_password = destination_password

    def execute_transfer(self, source_file_path, destination_file_path):
        source_transport = paramiko.Transport((self.source_host, self.source_port))
        source_transport.connect(
            username=self.source_username, password=self.source_password
        )
        source_client = paramiko.SFTPClient.from_transport(source_transport)

        destination_transport = paramiko.Transport(
            (self.destination_host, self.destination_port)
        )
        destination_transport.connect(
            username=self.destination_username, password=self.destination_password
        )
        destination_client = paramiko.SFTPClient.from_transport(destination_transport)

        try:
            source_file_size = source_client.stat(source_file_path).st_size
            last_position = 0

            with source_client.open(source_file_path, "rb") as source_file:
                with destination_client.open(
                    destination_file_path, "wb"
                ) as destination_file:
                    while last_position < source_file_size:
                        source_file.seek(last_position)
                        chunk = source_file.read(8192)  # Adjust chunk size if needed
                        destination_file.write(chunk)
                        last_position = source_file.tell()

        except (paramiko.SSHException, IOError) as e:
            print(f"Error moving file: {e}")
            raise
        finally:
            source_client.close()
            source_transport.close()
            destination_client.close()
            destination_transport.close()


# Example usage
source_host = "source_sftp.example.com"
source_port = 22
source_username = "source_username"
source_password = "source_password"

destination_host = "destination_sftp.example.com"
destination_port = 22
destination_username = "destination_username"
destination_password = "destination_password"

source_file_path = "/path/to/source/file.txt"
destination_file_path = "/path/to/destination/file.txt"

transfer = SFTPTransferToAnotherSFTP(
    source_host,
    source_port,
    source_username,
    source_password,
    destination_host,
    destination_port,
    destination_username,
    destination_password,
)
transfer.execute_transfer(source_file_path, destination_file_path)
