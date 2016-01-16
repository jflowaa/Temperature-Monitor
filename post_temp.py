import Adafruit_BBIO.ADC as ADC
import time
import requests

sensor_pin = 'P9_40'
ADC.setup()

while True:
    reading = ADC.read(sensor_pin)
    millivolts = reading * 1800
    temp_c = (millivolts - 500) / 10
    temp_f = (temp_c * 9/5) + 32
    r = requests.post("http://jflowaa.pythonanywhere.com/addrecord", data={"temperature": round(temp_f, 2)})
    print("Temperature: {} Post Request Status: {} {}".format(temp_f, r.status_code, r.reason))
    time.sleep(60 * 5)
