FROM apache/airflow:latest

USER root
RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

# RUN sudo apt-get -y install libpq-dev

COPY ./airflow/dags/common_functions /opt/airflow/dags/common_functions
COPY ./requirements.txt ./requirements.txt

USER airflow

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# RUN pip install /opt/airflow/common