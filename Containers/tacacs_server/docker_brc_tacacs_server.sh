#! /usr/bin/env bash
echo -e "\nRunning docker build-run-check script....\n\n"
docker stop tacacs_server
docker rm tacacs_server
docker build -t tacacs_server .
docker run -d -p 49:49 --name tacacs_server --restart unless-stopped tacacs_server
echo -e "\nChecking docker status....\n"
sleep 3
docker ps
