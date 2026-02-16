FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    gcc \
    make \
    git \
    libwrap0-dev \
    libpam0g-dev \
    libssl-dev \
    iputils-ping \
    flex \
    bison \
    sudo \
    vim \
    net-tools \
    iputils-ping \
    flex \
    autoconf \
    automake \
    libtool \
    pkg-config \
    build-essential \
    && apt-get clean

# Download and build TACACS+
RUN git clone https://github.com/kravietz/tac_plus.git /usr/local/src/tac_plus && \
    cd /usr/local/src/tac_plus && \
    ./configure && \
    make && \
    make install

# Create necessary directories
RUN mkdir -p /etc/tacacs+ /var/log/tacacs

# Add a sample TACACS+ configuration file
COPY tac_plus.cfg /etc/tacacs+/tac_plus.cfg

# Fix the local-lib.conf issue???
RUN echo "/usr/local/lib" > /etc/ld.so.conf.d/local-lib.conf
RUN ldconfig

# Expose TACACS+ default port (TCP 49)
EXPOSE 49

# Start TACACS+ server
CMD ["/usr/local/sbin/tac_plus", "-C", "/etc/tacacs+/tac_plus.cfg", "-G"]

