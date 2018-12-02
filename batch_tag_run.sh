#!/bin/bash
CWD=$(cd $(dirname $0); pwd)
if [ $# -ne 1 ]; then
  echo "Usage: $0 <TARGET_USER>"
  exit 0
fi
TARGET_USER=$1

TAG_FILES="$(aws s3 ls batch-instapy-sa/${TARGET_USER}/tag/ |awk '{print $4}')"
for TAG_FILENAME in ${TAG_FILES}; do
  echo "Execute tag_like \"${TAG_FILENAME}\""
  bash ${CWD}/tag_run.sh "${TARGET_USER}" "tag/${TAG_FILENAME}" >/dev/null 2>&1 &
  echo "Sleeping 60s for login periodicaly"
  sleep 60s
done
