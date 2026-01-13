# FROM ubuntu:22.04
FROM artifactory.itg.ti.com/docker-public/library/ubuntu:22.04

# set proxy server
ENV http_proxy=http://webproxy.ext.ti.com:80
ENV https_proxy=http://webproxy.ext.ti.com:80
ENV ftp_proxy=http://webproxy.ext.ti.com:80

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python and ldap dependencies
RUN apt-get update
RUN apt-get install python3 python3-pip python3-dev libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev libldap2-dev build-essential libssl-dev libffi-dev libmysqlclient-dev libjpeg-dev libpq-dev libjpeg8-dev liblcms2-dev libblas-dev libatlas-base-dev -y

# set work directory
WORKDIR /app/backend

# install python packages
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt --proxy=http://webproxy.ext.ti.com:80
# RUN pip3 install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy source files to container
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/app/backend/entrypoint.sh"]


