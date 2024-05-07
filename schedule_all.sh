#!/bin/bash 

# Update Satellite Information

wget -qr https://www.celestrak.com/NORAD/elements/weather.txt -O /home/linaro/wx-pi/weather.txt
grep "NOAA 15" /home/linaro/wx-pi/weather.txt -A 2 > /home/linaro/wx-pi/weather.tle
grep "NOAA 18" /home/linaro/wx-pi/weather.txt -A 2 >> /home/linaro/wx-pi/weather.tle
grep "NOAA 19" /home/linaro/wx-pi/weather.txt -A 2 >> /home/linaro/wx-pi/weather.tle



#Remove all AT jobs

for i in `atq | awk '{print $1}'`;do atrm $i;done

rm -f /home/linaro/wx-pi/upcoming_passes.txt

#Schedule Satellite Passes:

/home/linaro/wx-pi/schedule_satellite.sh "NOAA 19" 137.1000
/home/linaro/wx-pi/schedule_satellite.sh "NOAA 18" 137.9125
/home/linaro/wx-pi/schedule_satellite.sh "NOAA 15" 137.6200

python3 /home/linaro/wx-pi/sc-python/upload-upcoming-passes.py /home/linaro/wx-pi/upcoming_passes.txt
