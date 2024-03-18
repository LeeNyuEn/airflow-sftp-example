
from airflow_example.lib.target.sftp import SftpDataTargetManager


class DataTargetManagerFactory:
    @staticmethod
    def create_target_manager(target_type, **kwargs):
        if target_type == "sftp":
            return SftpDataTargetManager(**kwargs)
        else:
            raise ValueError(f"{target_type} is not supported")
