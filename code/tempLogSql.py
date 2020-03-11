import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import os

tempPin = 17

tempSensor = Adafruit_DHT.DHT11

GPIO.setmode(GPIO.BCM)
GPIO.setup(tempPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def readF(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempFahr = '{0:0.1f}*F'.format(temperature)
	else:
		print('Error Reading Sensor')
	return tempFahr

def readH(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	if humidity is not None and temperature is not None:
		humPer = '{0:0.1f}%'.format(humidity)
	else:
		print('Error Reading Sensor')
	return humPer


try:

	with open("../log/tempLogSql.csv", "a") as log:

		while True:
			time.sleep(60)
			dataTemp = readF(tempPin)
			dataHum = readH(tempPin)
			print (dataTemp)
			print (dataHum)
			log.write("{0},{1},{2}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(dataTemp),str(dataHum)))

except KeyboardInterrupt:
	os.system('clear')
	print('Thanks for Blinking and Thinking!')
	GPIO.cleanup()

