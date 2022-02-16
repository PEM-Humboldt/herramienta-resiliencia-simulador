FROM python:3.8-bullseye

ARG userpassword
RUN apt-get update && apt-get install -y openssh-server \
  && service ssh start \
  && useradd -ms /bin/bash model \
  && echo model:$userpassword | chpasswd

USER model
RUN mkdir -p /home/model/app
COPY . /home/model/app
WORKDIR /home/model/app/
RUN python3 -m pip install -r requirements.txt \
  && mkdir -p /home/model/app/outputs

USER root
CMD ["/usr/sbin/sshd","-D", "-e"]
