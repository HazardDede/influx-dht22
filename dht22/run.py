import Adafruit_DHT
import time
import calendar
import time
import logging
import os

from influxdb import InfluxDBClient

DATA_GPIO = int(os.environ.get('DATA_GPIO', '17'))
INFLUX_HOST = os.environ.get('INFLUX_HOST', 'influxdb')
INFLUX_PORT = int(os.environ.get('INFLUX_PORT', '8086'))
INFLUX_USER = os.environ.get('INFLUX_USER', 'root')
INFLUX_PWD = os.environ.get('INFLUX_PWD', 'root')
INFLUX_DATABASE = os.environ.get('INFLUX_DATABASE', 'smarthome')
HUMIDITY_PROTOCOL = os.environ.get('HUMIDITY_PROTOCOL', "humidity,room=living value={value}")
TEMPERATURE_PROTOCOL = os.environ.get('TEMPERATURE_PROTOCOL', "temperature,room=living value={value}")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_sensor_values():
	humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DATA_GPIO)
	return round(humidity, 2), round(temp, 2)

def save_sensor_values(humidity, temperature):
	ts = calendar.timegm(time.gmtime())
	temp_lp = TEMPERATURE_PROTOCOL.format(
		value=temperature,
		current_time=str(ts)
	)
	hum_lp = HUMIDITY_PROTOCOL.format(
		value=humidity,
		current_time=str(ts)
	)
	points = [temp_lp, hum_lp]
	client = InfluxDBClient(INFLUX_HOST, INFLUX_PORT, INFLUX_USER, INFLUX_PWD, INFLUX_DATABASE)
	client.write(points, {'db': INFLUX_DATABASE}, 204, 'line')

def loop():
	while True:
		humidity, temperature = get_sensor_values()
		logging.info("Temperature: {}, Humidity: {}".format(temperature, humidity))
		save_sensor_values(humidity, temperature)
		time.sleep(30)

def print_config():
	logging.info("DHT22 GPIO: {}".format(str(DATA_GPIO)))
	logging.info("INFLUX URI: influx://{user}:{pwd}@{host}:{port}/{db}".format(
		user=INFLUX_USER,
		pwd='x' * len(INFLUX_PWD),
		host=INFLUX_HOST,
		port=INFLUX_PORT,
		db=INFLUX_DATABASE
	))
	logging.info("Temperature line protocol: {}".format(TEMPERATURE_PROTOCOL))
	logging.info("Humidity line protocol: {}".format(HUMIDITY_PROTOCOL))

if __name__ == '__main__':
	print_config()
	loop()
