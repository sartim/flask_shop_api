FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    build-essential libssl-dev libffi-dev python3-dev \
    python3-pip python3-venv

# Setup flask application
RUN mkdir -p /home/ubuntu/app
ADD . /home/ubuntu/app
WORKDIR /home/ubuntu/app/

# Install python requirements
RUN pip3 install -r requirements.txt

# Start gunicorn server
ENTRYPOINT [ "gunicorn" ]
CMD ["--worker-class", "eventlet", "-w", "1", "wsgi:app"]