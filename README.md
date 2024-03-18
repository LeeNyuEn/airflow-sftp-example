# Introduction

Welcome! This project demonstrates using Airflow to automate file transfers between SFTP servers.

# Problem Statement
The objective is to develop an Apache Airflow DAG that facilitates the transfer of files
from the SFTP server at <source> to the SFTP server at \<target\> and ensures the
preservation of the original directory structure.
The synchronization process should be unidirectional; hence, any modification made on
\<target\> must not impact the <source>.
Deleted files on SFTP server at <source> must remain intact on \<target\> server.
# Installation
Clone the repository:
```bash
git clone https://github.com/LeeNyuEn/airflow-sftp-example.git
cd airflow-sftp-example
```

Build Airflow image, the default image name is `airflow_image_name`, if you changed the default value, remember to change it in the `.env` file also: 
```bash
sudo docker build -t <airflow_image_name> -f docker/Dockerfile.airflow .
```

Generate UUID:
```bash
 echo -e "AIRFLOW_UID=$(id -u)"
```

Open `.env` file and edit environment variables:
```toml
# Absolute path
AIRFLOW_PROJ_DIR="/home/nguyenle/Storage/project/airflow-sftp-example"  # Change to the absolutely path of the project

AIRFLOW_UID=1000  # UUID generated

# Image name to build Airflow
AIRFLOW_IMAGE_NAME="airflow_example_image"  # The Airflow image name has been built above

# Default Airflow username and password
_AIRFLOW_WWW_USER_USERNAME="airflow"
_AIRFLOW_WWW_USER_PASSWORD="airflow"
```

Init Airflow database:
```bash
sudo docker compose up airflow-init
```

Start Airflow services:
```bash
sudo docker compose up -d --build
```

Config Airflow connections and Variables, replace container name by  the correct one created:
```bash
sudo docker exec <airflow_exammple-airflow-webserver-1> airflow connections import config/connections.json
sudo docker exec <airflow_exammple-airflow-webserver-1> airflow variables import config/variables.json
```

# Usage
Access `http://localhost:8080` with default user name and password are `airflow`.

## Explaination
