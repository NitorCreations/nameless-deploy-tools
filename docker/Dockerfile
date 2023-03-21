FROM nitor/docker-base:latest

ENV LANG=C.UTF-8 \
  LC_ALL=C.UTF-8 \
  NODE_VERSION=17.8.0 \
  YARN_VERSION=1.22.18 \
  JAVA_HOME=/docker-java-home \
  GRADLE_VERSION=7.4.1 \
  MAVEN_VERSION=3.8.6 \
  LERNA_VERSION=4.0.0 \
  SERVERLESS_VERSION=3.10.0 \
  TERRAFORM_VERSION=1.1.7 \
  GRADLE_SHA256SUM=e5444a57cda4a95f90b0c9446a9e1b47d3d7f69057765bfb54bd4f482542d548
RUN curl -sL https://packages.microsoft.com/keys/microsoft.asc | \
  gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
  echo "deb [arch=$(dpkg --print-architecture)] https://packages.microsoft.com/repos/azure-cli/ bionic main" > /etc/apt/sources.list.d/azure-cli.list && \
  apt update && apt upgrade -y && apt install -y azure-cli dirmngr
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
  141F07595B7B3FFE74309A937405533BE57C7D57 \
  0704ADDF1D821345 \
  BF1518E0160788A2 \
  0704ADDF1D821345 \
  0A3939A4C560DD8B \
  C7BF26D0BB617866 \
  80CE7E5DC9725F3B \
  39BE51A1084C9113 \
  E136088A1824BDC1 \
  AC2D56EAF0E309FF \
  CC6CA38F5249885E \
  298E4C7A93CC521B \
  3B5B9D09699A35EB \
  3402A74A27CD9F92 \
  33CD6733AF5EC452 \
  0818D9D68FB67BAC \
  9B1FDA9F3C062231 \
  ABC8EE39BB550746 \
  FA383AABE50BC813 \
  0A335AF8B3A2D3B1 \
  2B7876099C0EFF85 \
  4F9BDB78DB596386 \
  B95BBD3FA43C4492 \
  E181870DC625BAFB \
  D2A765937BA507E8 \
  C92C5FEC70161C62 \
  873A8E86B4372146 \
  8F0FABD30F353251 \
  0B7B8BED064C851C \
  C2D879C8B0874707 \
  8FE7CB51365A46EF \
  A3F9CCC081C4177D \
  30E6F80434A72A7F \
  E8579C183571506F \
  A8AD2A7E9A25CE21 \
  3B58205B9D7013A9 \
  6525FD70CC303655 \
  7CADB77239332BA6 \
  2E2010F8A7FF4A41 \
  3E9B8F917F3ACFC4 \
  8C0AEE41CDA187E9 \
  C7CA19B7B620D787 \
  99A03029DDFA199E \
  CF277F2D2CF0CC82 \
  466CAED6E0747D50 \
  698DF224589628E0 \
  525875B36BFC416A \
  205C8673DC742C7C \
  1B2718089CE964B8 \
  AE5A7FB608A0221C \
  F704B943ED330E1B \
  F397D776F65C0178 \
  9C4F7E9D98B1CC53 \
  1FD507154FB9BA39 \
  EC61DFCD9B758417 \
  A5F094FD3961DF05 \
  1A2A1C94BDE89688 \
  CEBA9A9B905C7874 \
  00ECB4C4ED5885AC \
  0551FD3684FCBBB7 \
  EE2EBD8956CACE56 \
  105DE36038D8C6C5 \
  76C898A0C6C9B113 \
  C171A58398EEC284 \
  93450DF2DF9A3FA3 \
  012579464D01C06A \
  3632F7404A7EFFAF \
  DC08637CA615D22C \
  CA80D1F0EB6CA4BA \
  13D979595E6D01E1 \
  631E278529B5CB5F \
  9EB80E92EB2135B1 \
  A6310ACC4672475C \
  72D7468F \
  ; do \
  gpg --batch --keyserver hkp://keyserver.ubuntu.com --recv-keys "$key" || \
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
  && ARCH= && export dpkgArch="$(dpkg --print-architecture)" \
  && ln -svT "/usr/lib/jvm/java-17-openjdk-${dpkgArch}" /docker-java-home \
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
  && curl -SLO https://awscli.amazonaws.com/awscli-exe-linux-$(uname -m).zip \
  && curl -SLO https://awscli.amazonaws.com/awscli-exe-linux-$(uname -m).zip.sig \
  && gpg --verify awscli-exe-linux-$(uname -m).zip.sig awscli-exe-linux-$(uname -m).zip \
  && TMP_DIR=$(mktemp -d) && unzip awscli-exe-linux-$(uname -m).zip -d $TMP_DIR \
  && $TMP_DIR/aws/install -u \
  && rm -rf $TMP_DIR awscli-exe-linux-x86_64.zip.sig awscli-exe-linux-$(uname -m).zip \
  && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-$ARCH.tar.xz" \
  && curl -SLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
  && gpg --batch --decrypt --output SHASUMS256.txt SHASUMS256.txt.asc \
  && grep " node-v$NODE_VERSION-linux-$ARCH.tar.xz\$" SHASUMS256.txt | sha256sum -c - \
  && tar -xJf "node-v$NODE_VERSION-linux-$ARCH.tar.xz" -C /usr/local --strip-components=1 --no-same-owner \
  && rm "node-v$NODE_VERSION-linux-$ARCH.tar.xz" SHASUMS256.txt.asc SHASUMS256.txt \
  && ln -s /usr/local/bin/node /usr/local/bin/nodejs \
  && set -ex \
  && python -m pip install -U pip \
  && pip install -U --no-cache-dir ansible boto3 \
  && npm i -g npm \
  && npm i -g serverless@${SERVERLESS_VERSION} lerna@$LERNA_VERSION yarn@$YARN_VERSION \
  && curl -SLO "https://dlcdn.apache.org/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz" \
  && curl -SLO "https://downloads.apache.org/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz.asc" \
  && gpg --batch --verify apache-maven-${MAVEN_VERSION}-bin.tar.gz.asc apache-maven-${MAVEN_VERSION}-bin.tar.gz \
  && tar -xzf apache-maven-${MAVEN_VERSION}-bin.tar.gz -C /opt \
  && ln -snf /opt/apache-maven-${MAVEN_VERSION} /opt/maven \
  && ln -snf /opt/maven/bin/mvn /usr/bin/mvn \
  && rm -f apache-maven-${MAVEN_VERSION}-bin.tar.gz apache-maven-${MAVEN_VERSION}-bin.tar.gz \
  && curl -SLO "https://downloads.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip" \
  && echo "${GRADLE_SHA256SUM} gradle-${GRADLE_VERSION}-bin.zip" | sha256sum -c - \
  && unzip gradle-${GRADLE_VERSION}-bin.zip -d /opt \
  && rm gradle-${GRADLE_VERSION}-bin.zip \
  && ln -snf /opt/gradle-${GRADLE_VERSION} /opt/gradle \
  && ln -snf /opt/gradle/bin/gradle /usr/bin/gradle \
  && curl -o /usr/bin/lein "https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein" \
  && chmod 755 /usr/bin/lein && lein version \
  && curl -SLO "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${dpkgArch}.zip" \
  && curl -SLO "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_SHA256SUMS" \
  && curl -SLO "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_SHA256SUMS.sig" \
  && gpg --verify terraform_${TERRAFORM_VERSION}_SHA256SUMS.sig terraform_${TERRAFORM_VERSION}_SHA256SUMS \
  && grep " terraform_${TERRAFORM_VERSION}_linux_${dpkgArch}.zip" terraform_${TERRAFORM_VERSION}_SHA256SUMS | sha256sum -c - \
  && unzip -d /usr/bin terraform_${TERRAFORM_VERSION}_linux_${dpkgArch}.zip \
  && rm -f terraform_${TERRAFORM_VERSION}_linux_${dpkgArch}.zip terraform_${TERRAFORM_VERSION}_SHA256SUMS terraform_${TERRAFORM_VERSION}_SHA256SUMS.sig

RUN pip install --no-cache-dir nameless-deploy-tools==1.291

VOLUME /var/lib/docker

ENTRYPOINT ["dockerd-entrypoint.sh"]
