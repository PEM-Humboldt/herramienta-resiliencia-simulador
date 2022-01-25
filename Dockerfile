FROM python:3.8-bullseye

RUN apt-get update && apt-get install -y openssh-server
RUN service ssh start

RUN useradd -ms /bin/bash model
USER model

RUN mkdir -p /home/model/app
WORKDIR /home/model/app
COPY . /home/model/app
RUN python3 -m pip install -r requirements.txt

CMD ["python3"]
