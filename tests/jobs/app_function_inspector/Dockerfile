FROM python:3.6.14-alpine3.14 

WORKDIR /opt/ali/
COPY requirements.txt requirements.txt
COPY src src

RUN pip3 install -r requirements.txt

CMD ["python3", "src/runner.py"]