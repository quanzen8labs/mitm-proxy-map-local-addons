#!/bin/bash

TOOL="proxy"

if  [ -z "$1" ]
then
   TOOL="proxy"
else
   TOOL="$1";
fi

if [ $TOOL = "web" ]
then
    mitmweb -s map-local-addons.py
else
    mitmproxy -s map-local-addons.py
fi
