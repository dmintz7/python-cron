FROM debian:10

LABEL maintainer="dmintz"

RUN apt update
RUN apt-get install -y python3 python3-dev python3-pip git 
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY ./ /app
WORKDIR /app

RUN mkdir -p  /app/config
RUN mkdir -p  /app/logs
RUN mkdir -p  /app/repos
RUN mkdir -p  /app/mnt
ENV LOG_FOLDER=/app/logs

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/docker-entrypoint.sh
RUN ln -s usr/local/bin/docker-entrypoint.sh /
ENTRYPOINT ["docker-entrypoint.sh"]