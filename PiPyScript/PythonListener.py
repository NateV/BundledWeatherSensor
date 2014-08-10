# This script will run on a Raspberry Pi and loop, listening for Serial input from a 
# Arduino and temp/humidity sensor. It will store the sensor information in a sqlite
# database. 



import sqlite3 as sql
import serial
import re as regex


dbName = 'WeatherData'
sensorTable = "SensorData"
schema = "CREATE TABLE " + sensorTable + " ( id INTEGER PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, temp TEXT, humidity TEXT);"
conn = sql.connect(dbName + ".db")

requestPattern=regex.compile(".*\?temp=(.*)&humidity=(.*)")

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
  return "/dev/tty.usbmodem1411"
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
	  match = requestPattern.match(data)
	  if match: 
		temp = match.group(1)
		humidity = match.group(2)
		insertString = "INSERT INTO " + sensorTable + " (temp, humidity) VALUES ( '" + temp + "', '" + humidity + "');"
		print(insertString)
		cursor.execute(insertString)
		conn.commit()
		print(cursor)
		print("Sensor heard and recorded.")
	  else: 
		print("No sensor reading heard.")
	##end of while loop
except (KeyboardInterrupt, SystemExit):
  print("Exiting.")
  conn.commit()
  conn.close() 















