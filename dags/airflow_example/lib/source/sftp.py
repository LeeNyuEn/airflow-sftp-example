from typing import Iterator

from airflow_example.lib.source.base import DataSourceManager
from airflow_example.lib.connections.sftp import SftpManager


class SftpDataSourceManager(DataSourceManager, SftpManager):
    def fetch_data(
        self,
        source_file_path: str,
        chunk_size: int,
    ) -> Iterator[bytes]:
        self.get_sftp_client()
        with self.sftp_client.open(
            source_file_path, "rb", bufsize=chunk_size
        ) as source_file:
            while True:
                chunk = source_file.read(chunk_size)
                if not chunk:
                    break  # Exit the loop if no more data is read
                yield chunk
