import Adafruit_DHT
import time
import calendar
import time

from influxdb import InfluxDBClient

DATA_GPIO = 17
INFLUX_HOST = 'influxdb'
INFLUX_PORT = 8086
INFLUX_USER = 'root'
INFLUX_PWD = 'root'
INFLUX_DATABASE = 'smarthome'
HUMIDITY_PROTOCOL = "humidity,room=living value={value}"
TEMPERATURE_PROTOCOL = "temperature,room=living value={value}"

def get_sensor_values():
	humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DATA_GPIO)
	return round(humidity, 2), round(temp, 2)

def save_sensor_values(humidity, temperature):
	ts = calendar.timegm(time.gmtime())
	templp = TEMPERATURE_PROTOCOL.format(
		value=temperature,
		current_time=str(ts)
	)
	humlp = HUMIDITY_PROTOCOL.format(
		value=humidity,
		current_time=str(ts)
	)
	points = [templp, humlp]
	client = InfluxDBClient(INFLUX_HOST, INFLUX_PORT, INFLUX_USER, INFLUX_PWD, INFLUX_DATABASE)
	client.write(points, {'db': INFLUX_DATABASE}, 204, 'line')

def loop():
	while True:
		humidity, temperature = get_sensor_values()
		print(temperature, humidity)
		save_sensor_values(humidity, temperature)
		time.sleep(60)

if __name__ == '__main__':
	loop()
