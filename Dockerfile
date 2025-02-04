FROM python:3-slim
LABEL maintainer="marcel@dot-asterisk.nl"
ARG VERSION=2.24.1
USER root

WORKDIR /app

# Prerequisites
RUN apt update && apt install -y timidity ffmpeg

# Lilypond installation
ADD https://gitlab.com/lilypond/lilypond/-/releases/v$VERSION/downloads/lilypond-$VERSION-linux-x86_64.tar.gz ./
RUN mkdir /lilypond; tar -xf lilypond-$VERSION-linux-x86_64.tar.gz -C /lilypond; chown -R 1001:1001 /lilypond; mv /lilypond/lilypond-$VERSION/* /lilypond; rm -r /lilypond/lilypond-$VERSION;
RUN rm -rf lilypond-$VERSION-linux-x86_64.tar.gz

#Workdir creation
RUN mkdir -p /workdir
RUN chmod -R 777 /workdir && chown 1001:1001 /workdir

#App configuration
COPY . .
RUN pip install -r requirements.txt
USER 1001
EXPOSE 8080

ENTRYPOINT ["python", "run.py"]

