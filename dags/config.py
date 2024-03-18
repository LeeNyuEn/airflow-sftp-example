import os

from dynaconf import Dynaconf

current_folder = os.path.dirname(os.path.abspath(__file__))

settings = Dynaconf(
    settings_files=[
        f"{current_folder}/airflow_example/config/settings.toml",
    ],
)
