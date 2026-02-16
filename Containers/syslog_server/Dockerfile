FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y rsyslog vim

EXPOSE 514/udp

CMD ["rsyslogd", "-n"]
