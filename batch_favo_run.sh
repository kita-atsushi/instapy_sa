#!/bin/bash
CWD=$(cd $(dirname $0); pwd)
if [ $# -ne 1 ]; then
  echo "Usage: $0 <TARGET_USER>"
  exit 0
fi
TARGET_USER=$1

FAVO_FILES="$(aws s3 ls batch-instapy-sa/${TARGET_USER}/user/ |awk '{print $4}')"
for FAVO_FILENAME in ${FAVO_FILES}; do
  echo "Execute favo_like \"${FAVO_FILENAME}\""
  bash ${CWD}/favo_run.sh "${TARGET_USER}" "user/${FAVO_FILENAME}" >/dev/null 2>&1 &
  echo "Sleeping 60s for login periodicaly"
  sleep 60s
done
