#!/bin/bash

# Update Satellite Information

wget -qr https://www.celestrak.com/NORAD/elements/weather.txt -O INSTALL_DIR/weather.txt
grep "NOAA 15" INSTALL_DIR/weather.txt -A 2 > INSTALL_DIR/weather.tle
grep "NOAA 18" INSTALL_DIR/weather.txt -A 2 >> INSTALL_DIR/weather.tle
grep "NOAA 19" INSTALL_DIR/weather.txt -A 2 >> INSTALL_DIR/weather.tle



#Remove all AT jobs

for i in `atq | awk '{print $1}'`;do atrm $i;done

rm -f INSTALL_DIR/upcoming_passes.txt

#Schedule Satellite Passes:

INSTALL_DIR/schedule_satellite.sh "NOAA 19" 137.1000
INSTALL_DIR/schedule_satellite.sh "NOAA 18" 137.9125
INSTALL_DIR/schedule_satellite.sh "NOAA 15" 137.6200

python3 INSTALL_DIR/sc-python/upload-upcoming-passes.py INSTALL_DIR/upcoming_passes.txt
