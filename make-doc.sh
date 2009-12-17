#!/bin/bash
set -e

!git status > /dev/null && { echo "aborting - repo not clean. try git status"; exit 1; }

rm -rf /tmp/gh-pages
cd doc-src
rm -rf _build/html
make html
cp -a _build/html /tmp/gh-pages
cd ..

git checkout gh-pages
rm -rf *
cp -a /tmp/gh-pages/* .
git add .
git commit -m "update pages"

git checkout master

