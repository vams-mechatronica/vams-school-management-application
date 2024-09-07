FROM python:3
WORKDIR /vams/sms
COPY . /vams/sms
RUN pip install -r /vams/sms/requirements.txt
