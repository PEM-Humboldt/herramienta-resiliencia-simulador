FROM python:3.8-bullseye

ARG userpassword
RUN apt-get update && apt-get install -y openssh-server libaio1\
  && service ssh start \
  && useradd -ms /bin/bash model \
  && echo model:$userpassword | chpasswd

RUN wget https://download.oracle.com/otn_software/linux/instantclient/217000/instantclient-basic-linux.x64-21.7.0.0.0dbru.zip \
    && unzip instantclient-basic-linux.x64-21.7.0.0.0dbru.zip -d /opt/oracle/ \
    && cd /opt/oracle/instantclient* \
    && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci \
    && echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf \
    && ldconfig

USER model
RUN mkdir -p /home/model/app
COPY --chown=model . /home/model/app
WORKDIR /home/model/app/
RUN python3 -m pip install -r requirements.txt \
  && mkdir -p /home/model/app/outputs

USER root
CMD ["/usr/sbin/sshd","-D", "-e"]
