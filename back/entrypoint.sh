#!/bin/bash

# migrations
alembic upgrade head

sleep 5
python main.py
