import tkinter as tk
from tkinter import ttk
import pandas as pd


def load_data():
    data = pd.read_csv('downtime_log.csv')
    devices = {}
    
    for row in data.iterrows():
        device = row[1]['device']
        ip = row[1]['ip_address']
        timestamp = row[1]['timestamp']
        status = row[1]['status']
        
        if ip not in devices:
            devices[ip] = {
                'device': device,
                'ip_address': ip,
                'down_time': '',
                'up_time': '',
                'current_status': status
            }
        
        if status == 'down':
            devices[ip]['down_time'] = timestamp
        elif status == 'up':
            devices[ip]['up_time'] = timestamp
        
        devices[ip]['current_status'] = status
    
    return list(devices.values())

def update_table(data):
    for i in tree.get_children():
        tree.delete(i)
        
    for row in data:
        tree.insert('', tk.END, values=(row['device'], row['ip_address'], row['down_time'], row['up_time'], row['current_status']))

data = load_data()
root = tk.Tk()
root.title('Device Monitor')
columns = ('Device Name', 'IP Address', 'Down Time', 'Up Time', 'Current Status')
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill=tk.BOTH, expand=True)

update_table(data)

def refresh_data():
    new_data = load_data()
    update_table(new_data)
    root.after(10000, refresh_data)

refresh_data()

root.mainloop()
