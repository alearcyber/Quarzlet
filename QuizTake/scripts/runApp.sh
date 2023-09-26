#!/bin/bash

FLASK_APP="app:app"
WORKERS=2

# Check if there are any arguments
# Set default values if not
if [[ $ARGC==0 ]] then
    BIND=127.0.0.1:8000
else
    BIND=$1
fi

echo "gunicorn -w $WORKERS -b $BIND $FLASK_APP"
gunicorn -w $WORKERS -b $BIND $FLASK_APP