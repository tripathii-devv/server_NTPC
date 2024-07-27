import csv
import time
from datetime import datetime
from ping3 import ping, errors
import pandas as pd
import schedule
import os

devices = pd.read_csv('devices.csv')

downtime_log = 'downtime_log.csv'

previous_status = {device['ip_address']: 'unknown' for index, device in devices.iterrows()}

def check_availability():
    global previous_status

    file_exists = os.path.isfile(downtime_log)

    with open(downtime_log, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'device', 'ip_address', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        
        for index, device in devices.iterrows():
            ip = device['ip_address']
            name = device['name']
            status = "up"
            
            try:
                success_count = sum(ping(ip) is not None for _ in range(5))
                if success_count == 0:
                    status = "down"
                    
            except errors.PingError:
                status = "down"
            
            if previous_status[ip] != status:
                writer.writerow({
                    'timestamp': datetime.now(),
                    'device': name,
                    'ip_address': ip,
                    'status': status
                })
                
                previous_status[ip] = status

schedule.every(10).seconds.do(check_availability)

while True:
    schedule.run_pending()
    time.sleep(1)
