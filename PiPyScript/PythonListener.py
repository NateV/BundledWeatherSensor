# This script will run on a Raspberry Pi and loop, listening for Serial input from a 
# Arduino and temp/humidity sensor. It will store the sensor information in a sqlite
# database. 

import config

import sqlite3 as sql
import serial
import re as regex
import os

dbName = 'WeatherData'
sensorTable = "SensorData"
schema = "CREATE TABLE " + sensorTable + " ( id INTEGER PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, temp TEXT, humidity TEXT);"
conn = sql.connect(dbName + ".db")

dataPattern=regex.compile(".*\?temp=(.*)&humidity=(.*)")
offPattern = regex.compile(".*TURN_OFF.*")
offSignalCounter = 0;

#Check if the database exists. If not, create it.
def checkDB(): 
  try: 
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + sensorTable + "';")
    if len(cursor.fetchall())!=0: 
      print("Found the table.")
      print(cursor.fetchall())
    else:
      print("creating the table:")
      cursor.execute(schema)
  except sql.Error, e:
    print("Error: " + e.args[0])
## end of checkDB

#Find the serial port that the arduino is plugged into.
# For now, have to do this manually before running the script.
# To figure it out manually, use "ls /dev/tty*"
def findSerial():
  return config.LOCAL_SERIAL_PORT
  #return "/dev/tty.usbmodem1411"
# end of findSerial

#initialize
checkDB()
ser = serial.Serial(findSerial())
cursor = conn.cursor()



#insert into the database temp = match.group(1), humidity = match.group(2).
#main loop
try: 
	while(1):
	  data = ser.readline() #should be of the form "?temp=45&humidity=32"
	  dataMatch = dataPattern.match(data)
	  offMatch = offPattern.match(data)
	  if dataMatch: 
		#reset the offSignalCounter to 0 so that short presses of the button don't
		# turn off the device. Only a single long press should do that. 
		offSignalCounter = 0 
		temp = dataMatch.group(1)
		humidity = dataMatch.group(2)
		insertString = "INSERT INTO " + sensorTable + " (temp, humidity) VALUES ( '" + temp + "', '" + humidity + "');"
		print(insertString)
		cursor.execute(insertString)
		conn.commit()
		print(cursor)
		print("Sensor heard and recorded.")
	  elif offMatch:
	    offSignalCounter += 1
	    if offSignalCounter > 5:
	      raise Exception ("Shutting Down")
	  else: 
		print("No sensor reading heard.")
	##end of while loop
except (KeyboardInterrupt, SystemExit):
  print("Exiting.")
  conn.commit()
  conn.close() 
except Exception as e:
  print(e.args[0])
  conn.commit()
  conn.close()
  #keep commented unless using on the PI. Don't want to shut down the dev computer!
  #os.system("sudo shutdown -h now")















