FROM python:3.8-slim-buster

WORKDIR /app

COPY ./requirements.cfg .

RUN pip3 --no-cache install -r requirements.cfg

# RUN python3 -m nltk.downloader \
#         omw-1.4 \
#         stopwords \
#         wordnet \
#         -d usr/lib/nltk_data

COPY ./app/ .

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD [""]
