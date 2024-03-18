import abc
import stat
from typing import List, Tuple, Union

from airflow.providers.sftp.hooks.sftp import SFTPHook
from paramiko import SFTPClient, SFTPError, Transport


class SftpManager(abc.ABC):
    def __init__(
        self,
        *,
        host: Union[str, None] = None,
        port: Union[int, None] = None,
        username: Union[str, None] = None,
        password: Union[str, None] = None,
        hook: Union[SFTPHook, None] = None,
        directory: str = "/",
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.hook = hook
        self.directory = directory
        self.sftp_client: SFTPClient = None
        self.transport: Transport = None

    def get_sftp_client(self) -> None:
        if self.sftp_client is None:
            if self.hook:
                return self.hook.get_conn()
            else:
                try:
                    transport = Transport((self.host, self.port))
                    transport.connect(username=self.username, password=self.password)
                    self.sftp_client = SFTPClient.from_transport(transport)
                    self.transport = transport
                except Exception as e:
                    print(f"Error occurred during connect to sftp: {str(e)}")

    def close_connection(self) -> None:
        if self.sftp_client:
            self.sftp_client.close()
        if self.transport:
            self.transport.close()

    def create_directory_if_not_exists(self, directory: str) -> None:
        try:
            self.sftp_client.stat(directory)
        except FileNotFoundError:
            print(f"File not found, create new: {directory}")
            self.sftp_client.mkdir(directory)

    def create_directory_recursive(
        self,
        directories: List[str],
    ) -> None:
        for directory in directories:
            parts = directory.split("/")
            for i in range(1, len(parts)):
                partial_path = "/".join(parts[: i + 1])
                try:
                    self.sftp_client.stat(partial_path)
                except FileNotFoundError:
                    try:
                        self.create_directory_if_not_exists(partial_path)
                    except SFTPError as e:
                        print(f"Failed to create directory {partial_path}: {e}")

    def list_files(
        self, directory: Union[str, None] = None
    ) -> Tuple[List[str], List[str]]:
        directory = directory if directory else self.directory
        files = []
        directories = []

        def _list_files_recursively(remote_directory):
            directories.append(remote_directory)
            try:
                for item in self.sftp_client.listdir_attr(remote_directory):
                    item_path = remote_directory + "/" + item.filename
                    if stat.S_ISDIR(item.st_mode):
                        _list_files_recursively(item_path)
                    else:
                        files.append(
                            item_path,
                        )
            except FileNotFoundError:
                print("Folder not found")

        _list_files_recursively(directory)

        return files, list(set(directories))
