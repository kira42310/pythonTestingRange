FROM python:3
RUN apt-get update -y
RUN pip install pandas
RUN pip install matplotlib
