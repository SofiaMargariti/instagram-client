#!/bin/sh

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

commit_website_files() {
  git checkout master 
  git add translations/
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git remote add origin git@github.com:SofiaMargariti/instagram-client.git > /dev/null 2>&1
  git push --quiet --set-upstream origin master 
}

setup_git
commit_website_files
upload_files
