#!/bin/bash

set -x
set -u
set -e

exec > >(tee -i /tmp/deploy.log)
exec 2>&1

node ./node_modules/vite/bin/vite.js build --base=./
# cp "dist/" "/tmp/dist/"

cp dist/assets/scouter.*.js release/scouter.js

msg=`git log --oneline | head -n 1`

git checkout gh-pages

ls -l ./assets
rm -r ./assets

mv dist/* .

git add index.html assets/*
git commit -m "$msg"

git push origin gh-pages
git checkout main


