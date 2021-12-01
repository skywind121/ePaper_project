#!/bin/sh
#python epaperCode.py >/logs/epaperCode.log & python data.py >logs/data.log& python distance_sensor.py>logs/distance_sensor.log
python data.py & python epaperCode.py & python distance_sensor.py
