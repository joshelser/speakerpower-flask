#!/usr/bin/env bash

REPOSITORY="https://github.com/joshelser/speakerpower-flask.git"
INSTALL_DIR="/usr/local/speakerpower-flask.git"
VIRTUALENV_BASENAME="venv"
VIRTUALENV="${INSTALL_DIR}/${VIRTUALENV_BASENAME}"

if [[ ! -d ${INSTALL_DIR} ]]; then
    echo "Cloning repository"
    git clone ${REPOSITORY} ${INSTALL_DIR}
else
    echo "Updating repository"
    pushd ${INSTALL_DIR}
    git fetch && git reset --hard origin/master
    popd
fi

if [[ ! -d ${VIRTUALENV} ]]; then
    echo "Installing virtualenvironment"
    pushd $INSTALL_DIR
    virtualenv2 ${VIRTUALENV_BASENAME}
    ./${VIRTUALENV_BASENAME}/bin/pip install flask RPi.GPIO
    popd
else
    echo "Virtualenvironment already set up"
fi

echo "Starting application"
cd ${INSTALL_DIR}
FLASK_APP=speakerpower.py ./${VIRTUALENV_BASENAME}/bin/flask run --host=0.0.0.0 --port=80 >> /var/log/speakerpower.log 2>&1
