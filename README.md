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
To clone the repository:
```bash
git clone https://github.com/LeeNyuEn/airflow-sftp-example.git
cd airflow-sftp-example
```

To build the Airflow image, ensure you have Docker installed on your system. Execute the following command in terminal:
```bash
sudo docker build -t airflow_image_name -f docker/Dockerfile.airflow .
```
Replace `airflow_image_name` with the desired name for your Airflow image. If you've changed the default value, remember to update the `.env` file with the new image name.

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

Configure Airflow connections and variables, replacing container names with the correct ones created:
```bash
sudo docker exec airflow_exammple-airflow-webserver-1 airflow connections import config/connections.json
sudo docker exec airflow_exammple-airflow-webserver-1 airflow variables import config/variables.json
```

# Usage
To access the Airflow web interface, open a web browser and navigate to http://localhost:8080. Use the default username `airflow` and password `airflow` to log in.

# Explanation

## Coding principles
Code is written using **OOP** approach, by dividing it into basic components: **source**, **transform**, **target**, and **pipeline**. Each component has a distinct responsibility:

- **Source** and **target**: Handle the logic for fetching and sending data.
- **Transform**: A class used to perform specific data transformations.
- **Pipeline**: The main processing part responsible for managing how the components interact with each other, depending on processing needs and business requirements.

Each component has its own abstract and/or interface to ensure consistency and easy inheritance and extension if needed.

## Managing Configurations and Connections
Using Dynaconf to manage project configurations centrally. This allows us to handle all connection information, such as usernames and passwords, within a project. However, configuring all connections directly in the code increases the steps required for reconfiguration if any changes occur.
Therefore, I prefer storing connections in Airflow to centralize them and using variables to store configuration for DAGs and tasks. This approach provides more flexibility to update configurations if there are changes in business requirements and we can manage configurations more easily in the Airflow GUI.

## Code Styles
Using **flake8** as a linter and **black** as a formatter, I aim to maintain consistent code style as much as possible. However, I've found that some of flake8's style rules don't align with my preferences, so I've chosen to ignore them. This decision might lead to conflicts within a team, but they can be resolved easily.

As for the code formatter, I prefer **black** because it prioritizes content, logic, and bug fixes over styles. This approach helps prevent time wasted on debating code formatting preferences. But the black code style somehow did not using some habit like many pythoner are using, example like using double quotes instead of single quotes for string. While other formatter tools like yapf could address these issues, it raises the question: Why should I choose one style over another?

## Solution

### Sftp Transfer

Two straightforward approaches to transfer files from one SFTP server to another using Python and Airflow are:

- Utilizing SFTP Sensor and SFTP Hook in Airflow: This approach involves using Airflow's SFTP sensor to check if files are not exist on the target server. If not exist, downstream tasks are triggered to transfer the data file from the source server to the target server. However, implementing this idea might be challenging as there isn't a available implementation for it. One potential solution could be to extend the functionality of the existing SFTPHook and SFTPSensor classes, but this approach might require significant time and effort.
- Developing a Custom SFTP Module: Alternatively, I can develop a custom module, such as lib/sftp.py, to manage files in the SFTP servers. This module would contain a simple class with methods like listing files, creating directories, and connecting to SFTP servers. You can then use this module within your Airflow pipeline to implement the file transfer logic. This approach is more straightforward and easier to implement.

### Big file Transfer
In scenarios where large files, often gigabytes in size, need to be transferred via SFTP, memory issues on the server can lead to transfer delays or hang-ups. To mitigate this, I've implemented a chunked transfer method, sending data in manageable 4MB each packs between SFTP servers. While this approach resolves memory concerns, it presents its own challenge which is the transfer speeds are noticeably slower compared to direct SFTP commands. For instance, transferring a 1GB file on my development environment typically takes around 6 minutes, making it challenging to handle terabyte-sized files within small interval (5 to 10 minutes).

Idea: There are some ideas to solve this problem, but they have not been tested or tried yet. It may require time to investigate and verify if these solutions are effective:

- Develop a module using subprocess to download files locally and upload them using SFTP. We could utilize a BashOperator and a temporary folder for this purpose.
- Implement multithreading to transfer files by reading and writing data from specified positions in the file.
