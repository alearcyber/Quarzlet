#!/bin/bash


SCRIPT_DIR=$(pwd)
cd ..

FLASK_APP="app:app"
HOST=127.0.0.1
PORT=8000
WORKERS=2

# Check if there are any arguments
# Set default values if not
if [[ $ARGC==0 ]] then
    BIND=$HOST:$PORT
else
    BIND=$1
fi

echo "gunicorn -w $WORKERS -b $BIND $FLASK_APP"
gunicorn -w $WORKERS -b $BIND $FLASK_APP

cd $SCRIPT_DIR