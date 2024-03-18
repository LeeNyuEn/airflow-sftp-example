import abc
from typing import Union

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
