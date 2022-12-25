FROM public.ecr.aws/sam/build-python3.8

# Update the existing Amazon Linux packages
RUN user=root yum update -y

# Install some additional open-ssl packages & cmake & cargo (this will auto-install Rust)
RUN USER=root yum install openssl openssl-devel freetype-devel cmake g++ make cargo -y

# libssl-dev libffi-devel libfreetype6-dev
# Improve audio engine build output paths (include os and python version)

RUN USER=root yum install wget -y

# Lame installation from source (lame is not easily accessible trough public packages due to its licensing issues)
ENV LAME_VERSION=3.100

RUN wget http://jaist.dl.sourceforge.net/project/lame/lame/$LAME_VERSION/lame-$LAME_VERSION.tar.gz
RUN tar -xvf lame-$LAME_VERSION.tar.gz
WORKDIR ./lame-$LAME_VERSION
RUN ./configure && make && make install
# RUN USER=root ldconfig
# VOLUME /mp3
# WORKDIR /mp3
# ENTRYPOINT ["lame"]

WORKDIR /

# Install click (required to run the audio engine builder cli)
RUN USER=root pip install click