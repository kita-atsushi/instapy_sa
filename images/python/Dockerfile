FROM centos:7.4.1708


# Install python3.6
ENV PATH /usr/local/bin:$PATH
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum install -y python36u \
  python36u-libs \
  python36u-devel \
  python36u-pip

# Install chrome webdriver
RUN yum install -y unzip wget

ENV DOWNLOAD_URL "https://chromedriver.storage.googleapis.com/2.42/chromedriver_linux64.zip"
RUN wget "${DOWNLOAD_URL}" -P /tmp \
  && unzip /tmp/chromedriver_linux64.zip \
  && mv chromedriver /usr/local/bin/ \
  && chmod +x /usr/local/bin/chromedriver \
  && rm -f /tmp/chromedriver_linux64.zip

# For working dependencies
RUN yum install epel-release
RUN yum install -y libX11 GConf2 fontconfig

ENV GOOGLE_REPO_FILE="/etc/yum.repos.d/google-chrome.repo"
RUN echo '[google-chrome]' >>"${GOOGLE_REPO_FILE}" \
 && echo 'name=google-chrome' >>"${GOOGLE_REPO_FILE}" \
 && echo 'baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch' >>"${GOOGLE_REPO_FILE}" \
 && echo 'enabled=1' >>"${GOOGLE_REPO_FILE}" \
 && echo 'gpgcheck=1' >>"${GOOGLE_REPO_FILE}" \
 && echo 'gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub' >>"${GOOGLE_REPO_FILE}"

RUN yum install -y google-chrome-unstable libOSMesa google-noto-cjk-fonts

# Install selenium
COPY ./requirements.txt /requirements.txt
RUN pip3.6 install -r /requirements.txt
RUN pip3.6 install awscli

# Copy source
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
RUN mkdir -p /conf
COPY scripts/ /scripts/

# Copy sample config
COPY ./conf/interact_test.txt /interact_test.txt
COPY ./conf/black_list_test.txt /black_list_test.txt

ENTRYPOINT source /docker-entrypoint.sh
