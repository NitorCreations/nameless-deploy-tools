FROM nitor/docker-base:latest

ENV NODE_VERSION=14.16.0 \
 YARN_VERSION=1.22.10 \
 JAVA_HOME=/docker-java-home \
 GRADLE_VERSION=6.8.3 \
 MAVEN_VERSION=3.6.3 \
 PHANTOMJS_VERSION=2.1.1 \
 LERNA_VERSION=3.22.1 \
 SERVERLESS_VERSION=2.27.1 \
 TERRAFORM_VERSION=0.14.7 \
 TERRAFORM_SHA="6b66e1faf0ad4ece28c42a1877e95bbb1355396231d161d78b8ca8a99accc2d7"
RUN curl -sL https://packages.microsoft.com/keys/microsoft.asc | \
    gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ bionic main" > /etc/apt/sources.list.d/azure-cli.list && \
    apt-get update && apt-get upgrade -y && apt-get install -y openjdk-11-jdk git openssh-client unzip chromium-bsu jq gpg parallel dirmngr azure-cli
RUN set -ex \
  && groupadd --gid 1010 node \
  && useradd --uid 1010 --gid node --shell /bin/bash --create-home node \
  && groupadd --gid 1011 ndt \
  && useradd --uid 1011 --gid ndt --shell /bin/bash --create-home ndt \
  && for key in \
    94AE36675C464D64BAFA68DD7434390BDBE9B9C5 \
    FD3A5288F042B6850C66B31F09FE44734EB7990E \
    71DCFD284A79C3B38668286BC97EC7A07EDE3FC1 \
    DD8F2338BAE7501E3DD5AC78C273792F7D83545D \
    C4F0DFFF4E8C1A8236409D08E73BC641CC11F4C8 \
    B9AE9905FFD7803F25714661B63B535A4C206CA9 \
    56730D5401028683275BD23C23EFEFE93C4CFFFE \
    77984A986EBC2AA786BC0F66B01FBB92821C587A \
    4ED778F539E3634C779C87C6D7062848A1AB005C \
    B9E2F5981AA6E0CD28160D9FF13993A75599653C \
    8FCCA13FEF1D0C2E91008E09770F7A9A5AE15600 \
    A48C2BEE680E841632CD4E44F07496B3EB3C1762 \
    6A010C5166006599AA17F08146C2130DFD2497F5 \
  ; do \
    gpg --batch --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys "$key" || \
    gpg --batch --keyserver hkp://ipv4.pool.sks-keyservers.net --recv-keys "$key" || \
    gpg --batch --keyserver hkp://pgp.mit.edu:80 --recv-keys "$key" ; \
  done \
  && { \
		echo '#!/bin/sh'; \
		echo 'set -e'; \
		echo; \
		echo 'dirname "$(dirname "$(readlink -f "$(which javac || which java)")")"'; \
	} > /usr/local/bin/docker-java-home \
  && chmod +x /usr/local/bin/docker-java-home \
  && ARCH= && dpkgArch="$(dpkg --print-architecture)" \
  && ln -svT "/usr/lib/jvm/java-11-openjdk-${dpkgArch}" /docker-java-home \
  && if [ ! -d /usr/share/man/man1 ]; then \
		mkdir -p /usr/share/man/man1; \
	 fi \
  && case "${dpkgArch##*-}" in \
    amd64) ARCH='x64';; \
    ppc64el) ARCH='ppc64le';; \
    s390x) ARCH='s390x';; \
    arm64) ARCH='arm64';; \
    armhf) ARCH='armv7l';; \
    i386) ARCH='x86';; \
    *) echo "unsupported architecture"; exit 1 ;; \
  esac \
  && az bicep install && mv /root/.azure/bin/bicep /usr/local/bin/bicep \
  && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-$ARCH.tar.xz" \
  && curl -SLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
  && gpg --batch --decrypt --output SHASUMS256.txt SHASUMS256.txt.asc \
  && grep " node-v$NODE_VERSION-linux-$ARCH.tar.xz\$" SHASUMS256.txt | sha256sum -c - \
  && tar -xJf "node-v$NODE_VERSION-linux-$ARCH.tar.xz" -C /usr/local --strip-components=1 --no-same-owner \
  && rm "node-v$NODE_VERSION-linux-$ARCH.tar.xz" SHASUMS256.txt.asc SHASUMS256.txt \
  && ln -s /usr/local/bin/node /usr/local/bin/nodejs \
  && set -ex \
  && curl -fSLO --compressed "https://yarnpkg.com/downloads/$YARN_VERSION/yarn-v$YARN_VERSION.tar.gz" \
  && curl -fSLO --compressed "https://yarnpkg.com/downloads/$YARN_VERSION/yarn-v$YARN_VERSION.tar.gz.asc" \
  && gpg --batch --verify yarn-v$YARN_VERSION.tar.gz.asc yarn-v$YARN_VERSION.tar.gz \
  && mkdir -p /opt \
  && tar -xzf yarn-v$YARN_VERSION.tar.gz -C /opt/ \
  && ln -s /opt/yarn-v$YARN_VERSION/bin/yarn /usr/local/bin/yarn \
  && ln -s /opt/yarn-v$YARN_VERSION/bin/yarnpkg /usr/local/bin/yarnpkg \
  && rm yarn-v$YARN_VERSION.tar.gz.asc yarn-v$YARN_VERSION.tar.gz \
  && pip install -U --no-cache-dir ansible boto awscli boto3 nitor-vault \
  && npm i -g npm \
  && npm i -g serverless@${SERVERLESS_VERSION} lerna@$LERNA_VERSION \
  && wget -nv -O - "http://www.nic.funet.fi/pub/mirrors/apache.org/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz" | tar -xzf - -C /opt \
  && ln -snf /opt/apache-maven-${MAVEN_VERSION} /opt/maven \
  && ln -snf /opt/maven/bin/mvn /usr/bin/mvn \
  && wget -nv -O tmp.zip "https://downloads.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip" \
  && unzip tmp.zip -d /opt && rm tmp.zip \
  && ln -snf /opt/gradle-${GRADLE_VERSION} /opt/gradle \
  && ln -snf /opt/gradle/bin/gradle /usr/bin/gradle \
  && wget -nv -O - "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-${PHANTOMJS_VERSION}-linux-x86_64.tar.bz2" | tar -xjvf - \
  && mv phantomjs-*/bin/phantomjs /usr/bin \
  && rm -rf phantomjs-* \
  && wget -O /usr/bin/lein "https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein" \
  && chmod 755 /usr/bin/lein \
  && lein version \
  && curl -fSL "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" -o terraform.zip \
  && echo "${TERRAFORM_SHA} *terraform.zip" | sha256sum -c - \
  && unzip -d /usr/bin terraform.zip \
  && rm -f terraform.zip

RUN python -m pip install -U pip
RUN pip install --no-cache-dir nameless-deploy-tools==1.231

VOLUME /var/lib/docker

ENTRYPOINT ["dockerd-entrypoint.sh"]
