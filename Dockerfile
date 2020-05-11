FROM python:3.8-slim
# FROM python:3.7-slim

LABEL maintainer "Kyrylo Malakhov <malakhovks@nas.gov.ua> and Vitalii Velychko <aduisukr@gmail.com>"
LABEL description "Simple web service for computation of semantic similarity via word2vec pre-trained distributional semantic models (word embeddings)."

COPY . /srv/nor
WORKDIR /srv/nor

RUN apt-get -y clean \
    && apt-get -y update \
    && apt-get -y install nginx \
    && apt-get -y install python-dev \
    && apt-get -y install build-essential \
    # && apt-get -y install wget \
    && apt-get -y install curl \
    && apt-get -y install unzip \
    && pip install -r ./deploy/requirements.txt --src /usr/local/src \
    # && wget http://vectors.nlpl.eu/repository/20/95.zip \
    && curl http://vectors.nlpl.eu/repository/20/95.zip -o 95.zip \
    && unzip 95.zip -d ./tmp/ \
    && python -m spacy init-model nb ./tmp/nb_nowac_vectores --vectors-loc ./tmp/model.txt \
    && rm -r /root/.cache \
    && apt-get -y clean \
    && apt-get -y autoremove

COPY ./deploy/nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]