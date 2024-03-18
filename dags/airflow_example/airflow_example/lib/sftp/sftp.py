import abc
import stat
from typing import List, Union

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
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.hook = hook
        self.sftp_client: SFTPClient = self.get_sftp_client()

    def get_sftp_client(self):
        if self.hook:
            return self.hook.get_conn()
        else:
            try:
                transport = Transport((self.host, self.port))
                transport.connect(username=self.username, password=self.password)
                return SFTPClient.from_transport(transport)
            except Exception as e:
                print(f"Error occurred during connect to sftp: {str(e)}")

    def create_directory_if_not_exists(sftp_client, directory):
        try:
            sftp_client.stat(directory)
        except FileNotFoundError:
            sftp_client.mkdir(directory)

    def list_files(self, directory: str) -> List[str]:
        files = []

        def _list_files_recursively(remote_directory):
            for item in self.sftp_client.listdir_attr(remote_directory):
                item_path = remote_directory + "/" + item.filename
                if stat.S_ISDIR(item.st_mode):
                    _list_files_recursively(item_path)
                else:
                    files.append(item_path)

        _list_files_recursively(directory)

        return files
