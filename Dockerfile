#  creates a layer from the base Docker image.
FROM python:3.8.5-slim-buster

WORKDIR /app

ENV BRANCH_NAME Pyrogram
ENV DEBIAN_FRONTEND noninteractive
# http://bugs.python.org/issue19846
# https://github.com/SpEcHiDe/PublicLeech/pull/97
ENV LANG C.UTF-8
# https://shouldiblamecaching.com/
ENV PIP_NO_CACHE_DIR 1
ENV TZ Asia/Kolkata

# fix "ephimeral" / "AWS" file-systems
RUN sed -i.bak 's/us-west-2\.ec2\.//' /etc/apt/sources.list

# to resynchronize the package index files from their sources.
RUN apt -qq update

# base required pre-requisites before proceeding ...
RUN apt -qq install -y --no-install-recommends \
    curl \
    git \
    gnupg2 \
    unzip \
    wget

# add required files to sources.list
RUN wget -q -O - https://mkvtoolnix.download/gpg-pub-moritzbunkus.txt | apt-key add - && \
    wget -qO - https://ftp-master.debian.org/keys/archive-key-10.asc | apt-key add -
RUN sh -c 'echo "deb https://mkvtoolnix.download/debian/ buster main" >> /etc/apt/sources.list.d/bunkus.org.list' && \
    sh -c 'echo deb http://deb.debian.org/debian buster main contrib non-free | tee -a /etc/apt/sources.list'

RUN apt -qq update

# install required packages
RUN apt -qq install -y --no-install-recommends \
    # this package is required to fetch "contents" via "TLS"
    apt-transport-https \
    # install coreutils
    build-essential coreutils aria2 jq pv \
    # install encoding tools
    ffmpeg mediainfo rclone \
    # install extraction tools
    mkvtoolnix p7zip-full p7zip-rar \
    # miscellaneous helpers
    megatools mediainfo rclone && \
    # clean up the container "layer", after we are done
    rm -rf /var/lib/apt/lists /var/cache/apt/archives /tmp

# each instruction creates one layer
# Only the instructions RUN, COPY, ADD create layers.
# copies 'requirements', to inside the container
# ..., there are multiple '' dependancies,
# requiring the use of the entire repo, hence
RUN git clone https://github.com/SpEcHiDe/TerminalBot.git -b ${BRANCH_NAME} .

# install requirements, inside the container
RUN pip3 install --no-cache-dir -r requirements.txt

# specifies what command to run within the container.
CMD ["python3", "-m", "termbot"]
