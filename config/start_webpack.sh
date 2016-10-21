#!/bin/sh

rm -rf static/build/bundle.*
npm install && ./node_modules/.bin/webpack --watch --progress
