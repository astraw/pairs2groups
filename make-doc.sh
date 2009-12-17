#!/bin/bash
set -e

rm -rf doc/*
cd doc-src
rm -rf _build/html
make html
cp -a _build/html/* ../doc
