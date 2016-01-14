import requests
import random


rand_temp = random.uniform(0, 70)
r = requests.post("http://192.168.1.20:9090/addrecord", data={"temperature": rand_temp})
print(r.status_code, r.reason)

