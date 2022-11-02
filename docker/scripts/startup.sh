#!/bin/sh
# This script checks if the container is started for the first time.

CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    if [ -f "pants" ]
    then
        echo Pants already installed
    else
        curl -L -O https://static.pantsbuild.org/setup/pants 
        chmod +x ./pants
    fi
fi