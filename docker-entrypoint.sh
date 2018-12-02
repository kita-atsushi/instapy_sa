#!/usr/bin/env bash
# Parameter:
#  - INSTAPY_PARAMETER_USER         : Set run instapy_sa user
#  - INSTAPY_PARAMETER_STORE_PREFIX : Set aws parameter store prefix
#  - INSTAPY_S3_PREFIX              : Set batch-instapy-sa
#  - INSTAPY_S3_INTERACT_KEY        : Set s3 interact filepath key
#                                     e.g. "{type, user or tag}/{filepath}"
#  - INSTAPY_S3_BLACKLIST_KEY       : Set s3 interact blacklist key
#                                     e.g. "{type, user or tag}/blacklist"
# Usage:
#    export INSTAPY_PARAMETER_USER="instapy_sa_user"
#    export INSTAPY_PARAMETER_STORE_PREFIX="/batch/instapy_sa"
#    export INSTAPY_S3_PREFIX="batch-instapy-sa"
#    export INSTAPY_S3_INTERACT_KEY="user/follow_01"
#    export INSTAPY_S3_BLACKLIST_KEY="user/blacklist"

set -e

PS_PREFIX=${INSTAPY_PARAMETER_STORE_PREFIX:-}
PARAMETER_USER="${INSTAPY_PARAMETER_USER:-futmoji_k455}"
if [ -n "$PS_PREFIX" ]; then
    export ACCOUNT_USERNAME=`aws ssm get-parameters --name ${PS_PREFIX}/${PARAMETER_USER}/username --region ap-northeast-1 --query "Parameters[0].Value" --output text`
    export ACCOUNT_PASSWORD=`aws ssm get-parameters --name ${PS_PREFIX}/${PARAMETER_USER}/password --region ap-northeast-1 --query "Parameters[0].Value" --output text --with-decryption`
fi

S3_PREFIX=${INSTAPY_S3_PREFIX:-}
if [ -n "${S3_PREFIX}" ]; then
    INTERACT_FILE_URL="s3://${S3_PREFIX}/${PARAMETER_USER}/${INSTAPY_S3_INTERACT_KEY}"
    BLACKLIST_FILE_URL="s3://${S3_PREFIX}/common/${INSTAPY_S3_BLACKLIST_KEY}"
    export INTERACT_FILEPATH="/conf/`basename ${INSTAPY_S3_INTERACT_KEY}`"
    export BLACKLIST_FILEPATH="/conf/`basename ${INSTAPY_S3_BLACKLIST_KEY}`"
    aws s3 cp "${INTERACT_FILE_URL}" "${INTERACT_FILEPATH}"
    aws s3 cp "${BLACKLIST_FILE_URL}" "${BLACKLIST_FILEPATH}"
else
	# Set test file
    export INTERACT_FILEPATH="/interact_test.txt"
    export BLACKLIST_FILEPATH="/black_list_test.txt"
fi

exec "$@"
