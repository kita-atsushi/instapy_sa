#!/bin/bash

yum install -y unzip

VERSION="2.42"
FILENAME="chromedriver_linux64.zip"
URL="https://chromedriver.storage.googleapis.com/${VERSION}/${FILENAME}"
wget "${URL}" -P /tmp

unzip /tmp/${FILENAME}
mv ${FILENAME} /usr/local/bin/
chmod +x /usr/local/bin/${FILENAME}

rm -f /tmp/${FILENAME}

