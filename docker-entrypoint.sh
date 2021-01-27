#!/bin/bash

python3 /app/setup.py

touch /app/logs/*
tail -n0 -f /app/logs/*