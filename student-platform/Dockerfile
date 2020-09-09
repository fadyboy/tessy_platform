FROM python:3.8.5-alpine

RUN adduser -D studentapp

WORKDIR /home/studentapp

COPY requirements.txt requirements.txt
RUN apk update
RUN apk add --no-cache gcc \ 
                       g++ \
                       musl-dev \
                       jpeg-dev \
                       zlib-dev \
                       libffi-dev \
                       python3-dev \
                       cairo-dev \
                       pango-dev \
                       gdk-pixbuf-dev \
                       postgresql-dev \
                       && rm -rf /var/cache/apk/*
RUN python -m venv venv
RUN venv/bin/python -m pip install --upgrade pip wheel setuptools
RUN venv/bin/pip install -r requirements.txt

COPY studentapp studentapp
COPY migrations migrations
COPY student_platform.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP student_platform.py

RUN chown -R studentapp:studentapp ./
USER studentapp

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]