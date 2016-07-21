#!/bin/sh

sleep 2 && npm install && ./node_modules/.bin/webpack && python3 setup.py && python3 community_share_local_app.py
