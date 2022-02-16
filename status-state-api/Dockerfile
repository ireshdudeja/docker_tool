# base images
FROM python:3.9

WORKDIR /usr/app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

RUN apt-get update

RUN apt-get install docker.io -y

COPY ./server.py ./

CMD ["python3", "server.py"]