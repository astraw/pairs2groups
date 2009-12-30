#!/bin/bash
set -e

git status > /dev/null && { echo "aborting - repo not clean. try git status"; exit 1; }

rm -rf /tmp/gh-pages
cd doc-src
rm -rf _build/html
make html
cp -a _build/html /tmp/gh-pages
cd ..

git checkout gh-pages
git clean -dxf
git rm -r *
cp -a /tmp/gh-pages/* .
touch .nojekyll
find . | xargs git add
git commit -m "update pages"

git checkout master
