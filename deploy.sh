#!/bin/bash

# Copy Desired Files to Folder
rm -rf gh-pages
mkdir gh-pages
cp -r public/* gh-pages/

git add gh-pages
git commit -m "Update."

# Push Folder to Dedicated Branch
git subtree push --prefix gh-pages origin prod
git push origin origin/prod:master -f

