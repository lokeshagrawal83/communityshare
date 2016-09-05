FROM python:3-alpine

ADD . /communityshare
WORKDIR /communityshare

RUN \
    apk update && \
    apk add build-base postgresql-dev py-psycopg2 nodejs && \
    pip3 install -r /communityshare/requirements.txt && \
    pip3 install yapf

EXPOSE 5000
CMD /communityshare/start_dev.sh
