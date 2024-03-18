from datetime import timedelta
import pendulum

from airflow.decorators import dag, task


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
        import logging

        log = logging.getLogger(__name__)
        log.info("Lalala")
        print("Hello")

    sftp_file_transfer()


file_transfer()
