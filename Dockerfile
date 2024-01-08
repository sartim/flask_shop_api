FROM python:3.8.15-slim

ENV DEBIAN_FRONTEND noninteractive

ARG ENV
ARG PAGINATE_BY
ARG CACHED_QUERY
ARG REDIS_EXPIRE
ARG SECRET_KEY
ARG REDIS_URL
ARG DATABASE_URL
ARG ADMIN_EMAIL
ARG APP_EMAIL
ARG APP_EMAIL_PASSWORD
ARG ERROR

ENV ENV=$ENV
ENV PAGINATE_BY=$PAGINATE_BY
ENV REDIS_EXPIRE=$REDIS_EXPIRE
ENV SECRET_KEY=$SECRET_KEY
ENV REDIS_URL=$REDIS_URL
ENV DATABASE_URL=$DATABASE_URL
ENV ADMIN_EMAIL=$ADMIN_EMAIL
ENV APP_EMAIL_PASSWORD=$APP_EMAIL_PASSWORD
ENV ERROR=$ERROR

RUN apt-get update && apt-get install -y \
    build-essential libssl-dev libffi-dev python3-dev \
    python3-pip python3-venv redis-server wget python3.8-dev

#RUN cd /usr/src && \
#    wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz && \
#    tar xzf Python-3.8.10.tgz && \
#    cd Python-3.8.10 && \
#    ./configure --enable-optimizations && \
#    make install

# Setup flask application
RUN mkdir -p /home/ubuntu/app
ADD . /home/ubuntu/app
WORKDIR /home/ubuntu/app/

# Install python requirements
RUN pip3 install -r requirements.txt

# Start gunicorn server
ENTRYPOINT [ "gunicorn" ]
CMD ["--worker-class", "eventlet", "-w", "1", "wsgi:app"]
