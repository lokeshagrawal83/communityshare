FROM python:3-alpine

COPY ./requirements.txt /communityshare/requirements.txt
WORKDIR /communityshare

RUN apk add --no-cache --virtual .build-deps \
        build-base \
        postgresql-dev \
        py-psycopg2 \
    && apk add --no-cache \
        nodejs \
    && pip3 install -r /communityshare/requirements.txt \
    && pip3 install yapf \
    && python -m pip uninstall pip setuptools -y \
    # This reduction taken from…
    # http://nickjanetakis.com/blog/alpine-based-docker-images-make-a-difference-in-real-world-apps
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/* \
    && rm -rf /root/.cache/pip/* \
    && rm -rf /communityshare
