import time
import random
import datetime

def get_id(type):
    table={
        "role":"90",
        "authority":"80",
        "family":"70",
        "volun_activity":"60",
        "respect":"50",
        "product":"40",
        "product_type":"30",
        "community":"20",
        "user":"10",
        "in_code":"001",
        "dai":"01",
        "zupu":"z",
        "phone_code":""
    }
    t = time.time()
    if type=="in_code":
        return str(int(random.uniform(1, 3) * 1000))
    if type == "phone_code":
        return str(int(random.uniform(1, 3) * 1000))
    rd = str(int(random.uniform(1, 3) * 1000))+str(int(t))
    return table[type]+rd


