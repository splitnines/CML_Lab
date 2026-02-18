FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y freeradius freeradius-utils vim iproute2 iputils-ping && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./freeradius /etc/freeradius

EXPOSE 1812/udp 1813/udp

CMD ["freeradius", "-X"]
