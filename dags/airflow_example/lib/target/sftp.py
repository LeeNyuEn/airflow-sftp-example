from typing import Iterator

from airflow_example.lib.target.base import DataTargetManager
from airflow_example.lib.connections.sftp import SftpManager


class SftpDataTargetManager(DataTargetManager, SftpManager):
    def ingest_data(
        self,
        destination_file_path: str,
        chunks: Iterator[bytes],
    ) -> None:
        with self.sftp_client.open(destination_file_path, "ab") as destination_file:
            destination_file.set_pipelined(True)
            for chunk in chunks:
                destination_file.write(chunk)
