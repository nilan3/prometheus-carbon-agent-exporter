FROM python:3.5-slim-jessie

########### INSTALL PYTHON WORK DIR ###########

RUN mkdir /prom_carbon_exporter
WORKDIR /prom_carbon_exporter

########### INSTALL PYTHON APP REQUIREMENTS ###########

COPY requirements.txt /prom_carbon_exporter/requirements.txt
COPY app /prom_carbon_exporter/app

RUN chmod +x /prom_carbon_exporter/app/collector.py \
&& pip install -r requirements.txt
