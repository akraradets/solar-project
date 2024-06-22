FROM ubuntu:22.04

ARG WORKDIR=/workspaces/solar-project
ARG VENDOR=""
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=${WORKDIR}:${VENDORDIR}
ENV PIPENV_VENV_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR ${WORKDIR}
ARG DEBIAN_FRONTEND=noninteractive
# Timezone
ENV TZ="Asia/Bangkok"

# https://github.com/pyenv/pyenv/wiki#suggested-build-environment
RUN apt update && apt upgrade -y
RUN apt install -y build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev curl \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
# Set timezone
RUN apt install -y tzdata
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
# Set locales
# https://leimao.github.io/blog/Docker-Locale/
RUN apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LC_ALL en_US.UTF-8 
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  

RUN apt install -y python3 python3-pip

RUN pip install poetry==1.8.3
RUN pip install poethepoet==0.26.1

# GDAL
RUN apt install -y gdal-bin libgdal-dev
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
RUN pip3 install GDAL==3.4.1

# Clear apt for optimizing image size
RUN apt clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
