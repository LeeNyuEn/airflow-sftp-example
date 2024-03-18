import abc
import stat
from typing import List, Tuple, Union

from airflow.providers.sftp.hooks.sftp import SFTPHook
from paramiko import SFTPClient, Transport


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
        self.sftp_client: SFTPClient = self.get_sftp_client()

    def get_sftp_client(self) -> SFTPClient:
        if self.hook:
            return self.hook.get_conn()
        else:
            try:
                transport = Transport((self.host, self.port))
                transport.connect(username=self.username, password=self.password)
                return SFTPClient.from_transport(transport)
            except Exception as e:
                print(f"Error occurred during connect to sftp: {str(e)}")

    def create_directory_if_not_exists(sftp_client, directory) -> None:
        try:
            sftp_client.stat(directory)
        except FileNotFoundError:
            print(f"File not found, create new: {directory}")
            sftp_client.mkdir(directory)

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
