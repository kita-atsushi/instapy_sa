#!/bin/bash
yum install epel-release
yum install -y libX11 GConf2 fontconfig

cat <<'EOF' >/etc/yum.repos.d/google-chrome.repo
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
EOF
yum install -y google-chrome-unstable libOSMesa google-noto-cjk-fonts
