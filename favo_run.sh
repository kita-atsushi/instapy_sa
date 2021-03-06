#!/bin/bash
CWD=$(cd $(dirname $0); pwd)

export PYTHONUNBUFFERED=0
INSTAPY_IMAGE="${INSTAPY_IMAGE:-instapysa_selenium:latest}"
INSTAPY_PARAMETER_USER="${1:-futmoji_k455}"
INSTAPY_S3_INTERACT_KEY="${2:-user/follow_01}"

# Envrionment: AWS_ACCESS_KEY_ID required.
#              AWS_SECRET_ACCESS_KEY required.

function favo_like {
  INTERACT_KEY_BASENAME=`basename ${INSTAPY_S3_INTERACT_KEY}`
  echo "@@@ Running favo_run"
  docker run --rm \
    --name favo_${INTERACT_KEY_BASENAME} \
    --env AWS_DEFAULT_REGION="ap-northeast-1" \
    --env AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    --env AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    --env INSTAPY_PARAMETER_USER="${INSTAPY_PARAMETER_USER}" \
    --env INSTAPY_PARAMETER_STORE_PREFIX="/batch/instapy_sa" \
    --env INSTAPY_S3_PREFIX="batch-instapy-sa" \
    --env INSTAPY_S3_INTERACT_KEY="${INSTAPY_S3_INTERACT_KEY}" \
    --env INSTAPY_S3_BLACKLIST_KEY="user/blacklist" \
    --env INTERACT_AMOUNT="1" \
    --env INTERACT_RATIO="100" \
    "${INSTAPY_IMAGE}" \
    -- python3.6 -u "/scripts/favorite.py"
}

favo_like
