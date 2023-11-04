#!/bin/bash


SCRIPT_DIR=$(pwd)
cd /app
echo "Running from $(pwd)"

FLASK_APP="app:app"
HOST=0.0.0.0
PORT=8000
BIND=$HOST:$PORT
WORKERS=2

# Check if there are any arguments
# Set default values if not
# if [[ $ARGC==0 ]] then
#     BIND=$HOST:$PORT
# else
#     BIND=$1
# fi

echo "gunicorn -w $WORKERS -b $BIND $FLASK_APP"
gunicorn -w $WORKERS -b $BIND $FLASK_APP

cd $SCRIPT_DIR