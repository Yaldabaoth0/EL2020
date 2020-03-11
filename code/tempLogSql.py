import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import os
import sqlite3 as sql
import smtplib

#GLOBALS
tempPin = 17
redPin = 27
greenPin = 22

#TempHum Sensor
tempSensor = Adafruit_DHT.DHT11

blinkDur = .1

blinkTime = 7


GPIO.setmode(GPIO.BCM)
GPIO.setup(tempPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)



con = sql.connect('../log/tempLog.db')
cur = con.cursor()


#Checkbit is initialized to 0. Will throw a warning when run, but will still work just fine.
eChk = 0


def readF(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempFahr = '{0:0.1f}'.format(temperature)
	else:
		print('Error Reading Sensor')
	return tempFahr

def readH(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	if humidity is not None and temperature is not None:
		humPer = '{0:0.1f}'.format(humidity)
	else:
		print('Error Reading Sensor')
	return humPer


oldTime = 60

try:

	with open("../log/tempLogSql.csv", "a") as log:

		while True:

			if time.time() - oldTime > 59:
				dataTemp = readF(tempPin)
				dataHum = readH(tempPin)
				cur.execute('insert into tempLog values(?,?,?)', (time.strftime('%Y-%m-%d %H:%M:%S'),dataTemp,dataHum))
				con.commit()
				table = con.execute("select * from tempLog")
				os.system('clear')
				print "%-30s %-20s %-20s" %("Date/Time", "Temp", "Humidity")
				for row in table:
					print "%-30s %-20s %-20s" %(row[0], row[1], row[2])
				oldTime = time.time()

except KeyboardInterrupt:
	os.system('clear')
	print('Thanks for Blinking and Thinking!')
	GPIO.cleanup()

