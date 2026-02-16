FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    snmp snmpd snmptrapd curl wget unzip vim \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/share/snmp/mibs/cisco

ADD mibs.zip /tmp/mibs.zip
RUN unzip /tmp/mibs.zip -d /usr/share/snmp/mibs/cisco

ENV MIBS=+ALL

EXPOSE 162/udp

RUN mkdir -p /etc/snmp

COPY snmptrapd.conf /etc/snmp/snmptrapd.conf

CMD ["snmptrapd", "-f", "-Le"]
