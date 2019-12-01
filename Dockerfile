FROM python:3.6

MAINTAINER Mirza Musharaf Baig<musharaf715@gmail.com>

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
	git \
	python \
	uuid-runtime \
	python3-dev \
	python-setuptools \
	python3-pip \
	python-pycurl \
	nginx \
    libwebp-dev \
	default-libmysqlclient-dev \
	libpq-dev \
    python3-pip


RUN pip install setuptools
#RUN pip install --upgrade pip

WORKDIR /home/docker/code/

ADD . /home/docker/code/

RUN pip install -r requirements/base.txt

RUN chmod +x entry_point.sh

ENV DJANGO_SETTINGS_MODULE='PizzaOnline.settings'

CMD ["./entry_point.sh"]

#EXPOSE 8000