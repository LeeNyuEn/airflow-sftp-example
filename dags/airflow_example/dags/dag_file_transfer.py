from datetime import timedelta
from airflow.providers.sftp.hooks.sftp import SFTPHook
import pendulum

from airflow.decorators import dag, task

from airflow_example.lib.pipeline import SftpFileTransferPipeline


@dag(
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=10),
    },
    schedule="@hourly",
    start_date=pendulum.datetime(2024, 3, 18, tz="UTC"),
    catchup=False,
    tags=["etl", "sftp"],
)
def file_transfer():
    @task
    def sftp_file_transfer():
        sftp_transfer_pipeline = SftpFileTransferPipeline(
            source_config={
                "hook": SFTPHook(
                    ssh_conn_id="sftp_source",
                ),
            },
            target_config={
                "hook": SFTPHook(
                    ssh_conn_id="sftp_target",
                ),
            },
        )
        sftp_transfer_pipeline.run()

    sftp_file_transfer()


file_transfer()
