FROM python:3.8-slim

LABEL maintainer "Kyrylo Malakhov <malakhovks@nas.gov.ua> and Vitalii Velychko <aduisukr@gmail.com>"
LABEL description "nb-terms is an NLU-powered network toolkit (Web service with API) for the contextual and semantic analysis of the natural language text messages (Norwegian Bokmål)."

COPY . /srv/nor
WORKDIR /srv/nor

RUN apt-get -y clean \
    && apt-get -y update \
    && apt-get -y install nginx \
    && apt-get -y install python-dev \
    && apt-get -y install build-essential \
    # && apt-get -y install curl \
    # && apt-get -y install unzip \
    # for hunspell https://github.com/blatinier/pyhunspell
    && apt-get -y install libhunspell-dev \
    # ------------------------------------------------------------------
    && pip install -r ./deploy/requirements.txt --src /usr/local/src \
    && rm -r /root/.cache \
    && apt-get -y clean \
    && apt-get -y autoremove

COPY ./deploy/nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]