FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    build-essential libssl-dev libffi-dev python3-dev \
    python-pip python3.5 python3-venv

# Setup flask application
RUN mkdir -p /home/ubuntu/app
ADD ./app /home/ubuntu/app
ADD ./tests /home/ubuntu/app
ADD manage.py /home/ubuntu/app
ADD wsgi.py /home/ubuntu/app
ADD requirements.txt /home/ubuntu/app
ADD README.md /home/ubuntu/app
WORKDIR /home/ubuntu/app/

# Upgrade pip
RUN pip install --upgrade pip
# Install python requirements
RUN pip install -r requirements.txt

ENTRYPOINT [ "gunicorn" ]

CMD ["--worker-class", "eventlet", "-w", "1", "wsgi:app"]