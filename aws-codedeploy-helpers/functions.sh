#!/usr/bin/env bash

before_install() {
    rm -rf /home/ubuntu/flask_shop_api
}

after_install() {
    echo "pass"
}

application_start() {
    supervisorctl start all
}

application_stop(){
    supervisorctl stop all
}
