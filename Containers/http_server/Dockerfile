FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# Install nginx and vim, of course because I'll need to edit shit
RUN apt-get update && apt-get install -y \
    nginx \
    vim \
    && apt-get clean

# server root directory
WORKDIR /var/www/html
COPY root/ .

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
