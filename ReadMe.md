#Wifi Weather Station Version: One Big Happy

This version connects the sensor to an Arduino, and then connects the Arduino 
directly to a Raspberry Pi. The the Arduino sends sensor data over the Serial
connection to the Pi. The Pi is running a simple script that reads the Serial input
and then stores the temperature and humidity information in a mongo database. 

## Components:

- Electronics
--Arduino
--Raspberry pi
--USB connector
--LED
--Button
--DHT11 Temp/humidy sensor

- Arduino Sketch

- Python script

## Instructions

### For setting up
1. Clone github repository on a Pi running Raspbian
2. If you use virtualenv for Python, then set up a virtual environment and install the 
required modules using the requirements.txt.
3. Connect the arduino and push the sketch to the arduino.
4. Run the script PythonListener.py
5. You do not need shell access to the Pi for the device to keep collecting data. At this
point, you could disconnect from the Pi and put the sensor somewhere discrete and let it
do its thing. Just make sure it has power, of course. 

### For shutting down
1. If you still have shell access to the Pi, then Control C will terminate the script and 
properly close the database connection. 
2. If you do not have shell access, press and hold the button down. After 5-10 seconds, 
the Pi will close the database connection, end the script, and shut down safely. 

## Thoughts
  

### Features
1. This is a big improvement. Its pretty self contained and could be used anywhere. 
2. It can be shut down with a physical button. So once you start the sensor, you don't need to 
maintain a connection to it. And you don't need to reconnect to shut it down. 
3. SQLite3, which is the database layer of the program, seems to work very well with Pi. 
To get access to the database, it is just a matter of copying the single database file to
wherever else you'd like it to be. 

### Limitations
1. Right now you do still need to connect to the Pi to get it going. A more convenient setup
would have the sensor start collecting data automatically without needing a laptop or other
interface. It would be pretty simple to set that up--all that would be necessary would be
a shell script that runs on startup of the Pi. I haven't done that because that would make
the pi less useful for other tasks, and I simply have not committed to using the Pi I have
for only this purpose.
2. It could be more convenient to access the data. Copying a database file works, but its 
inelegant and not user friendly. One might also run a python server with and API
on the Pi to enable logging into the server to view or collect the information. 