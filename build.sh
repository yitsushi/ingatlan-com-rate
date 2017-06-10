#!/bin/bash

CWD=$(pwd)
PROJECT_DIR=$(dirname $0)
BUILD_DIR=$PROJECT_DIR/build/$(date +"%s")

if [ ! -d "$PROJECT_DIR/build" ]; then
  mkdir $PROJECT_DIR/build
fi

mkdir $BUILD_DIR

rsync -ra --exclude='.git*' --exclude='build.sh' --filter=':- .gitignore' ./ $BUILD_DIR

cd $BUILD_DIR
tar -zcvf ../output.tar.gz ./
cd $CWD

rm -rf $BUILD_DIR
