FROM python:3.8.0-slim-buster
LABEL maintainer="chilledgeek@gmail.com"
ARG VERSION=2.24.0
USER root

WORKDIR /

ADD https://gitlab.com/lilypond/lilypond/-/releases/v$VERSION/downloads/lilypond-$VERSION-linux-x86_64.tar.gz ./

RUN mkdir /lilypond; tar -xf lilypond-$VERSION-linux-x86_64.tar.gz -C /lilypond; chown -R 1001:1001 /lilypond; mv /lilypond/lilypond-$VERSION/* /lilypond; rm -r /lilypond/lilypond-$VERSION;

RUN rm -rf lilypond-$VERSION-linux-x86_64.tar.gz

RUN mkdir -p /workdir
RUN chmod -R 777 /workdir

WORKDIR /
COPY . /

RUN pip install -r requirements.txt

USER 1001

EXPOSE 8080

ENTRYPOINT ["python", "run.py"]

