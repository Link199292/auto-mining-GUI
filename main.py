import tkinter as tk
import tkinter.filedialog
import time
import os
import psutil
import datetime
import requests
import subprocess
from datetime import datetime, timedelta

def file_name():
    '''
    ask for miner file name if not already provided
    '''
    with open('directory.txt', encoding = 'utf-8') as r:
        file = r.readline()
    if file:
        return
    dial = tk.Tk()
    dial.iconbitmap("icon.ico")
    dial.withdraw()
    file = tk.filedialog.askopenfilename(title = "Select miner's bat file")
    with open('directory.txt', 'w') as w:
        w.write(file)
    dial.destroy()

def read_config():
    '''read config values, store it in diz and return it
    '''
    with open('config.txt', encoding = 'utf-8') as r:
        file = r.read()
        diz = eval(file)
    return diz

def get_time():
    x = datetime.datetime.now()
    current = x.strftime('%D - %H:%M:%S')
    return current

def which_miner():
    '''if lolminer return (filename, processname)
       else return(filename, processname)
    '''
    with open('directory.txt', encoding = 'utf-8') as r:
        line = r.readline()
    if line.endswith('mine_eth.bat'):
        return ('mine_eth.bat', 'lolMiner.exe')
    elif line.endswith('ETH-ethermine.bat'):
        return ('ETH-ethermine.bat', 't-rex.exe')

def reset_timer():
    global wait_time_inactive
    global wait_time_active
    wait_time_inactive = diz['wait_time_inactive'] 
    wait_time_active = diz['wait_time_active']
    
def get_value():
    diz = read_config()
    api = diz['API']
    start_gas = diz['start_gas_threshold']
    stop_gas = diz['stop_gas_threshold']
    oracle = diz['gas_oracle']
    attempt = 0
    url = f'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={api}'
    req = requests.get(url)
    if req.status_code == 200:
        x = eval(req.text)
        text_connection.set('Connected')
        connection_attempt.config(fg = 'green')
        v = x['result'][oracle]
        text_gas.set(v)
        if int(v) >= start_gas:
            gas_label.config(fg = 'green')
        else:
            gas_label.config(fg = 'red')
        return v
    else:
        attempt += 1
        text_connection.set(text = f'reconnecting: {attempt}')
        connection_attempt.config(fg = 'red')
        text_connection.after(1000, get_value)
    
def decide():
    global started
    global miner
    diz = read_config()
    start_gas = diz['start_gas_threshold']
    stop_gas = diz['stop_gas_threshold']
    val = int(get_value())
    if started and val < stop_gas:
        started = False
        stop_miner()
    if not started and val >= start_gas:
        started = True
        start_miner()

def running():
    if miner[1] in (p.name() for p in psutil.process_iter()):
        return True
    return False

def check_process_running():
    x = running()
    if x:
        text_status.set('Running')
        status_label.config(fg = 'green')
    else:
        text_status.set('Not running')
        status_label.config(fg = 'red')
    status_label.after(1000, check_process_running)

def start_miner():
    global file
    global started
    reset_timer()
    x = running()
    if not x:
        save = os.getcwd()
        os.chdir('/'.join(file.split('/')[:-1]))
        file = miner[0]
        os.system(f'start cmd /k {file}')
        text_status.set('Running')
        status_label.config(fg = 'green')
        os.chdir(save)
        started = True
        
def stop_miner():
    reset_timer()
    global started
    x = running()
    if x:
        command = f'taskkill /im {miner[1]} /t /f'
        string = subprocess.getoutput(command)
        string = string.split('(')[-1]
        string = ''.join([i for i in string if i.isnumeric()])
        os.system(f'taskkill /pid {string} /t /f')
    text_status.set('Stopped')
    status_label.config(fg = 'red')
    started = False

################################################################################

#ask for folder and load config.txt

file = file_name()
diz = read_config()

started = False
miner = which_miner()
wait_time_active = diz['wait_time_active']
wait_time_inactive = diz['wait_time_inactive']

root = tk.Tk()

#main page
root.title('auto-mining')
root.geometry('400x500')
root.resizable(0, 0)

#change icon
root.iconbitmap("icon.ico")

#background image
img = tk.PhotoImage(file = 'miningmod2.png')
image = tk.Label(root, image = img)
image.place(x = -83, y = 232)

#status label
txt = tk.Label(root, text = 'Status:', fg = 'black', bg = 'lightgrey', font = 'Helvetica 10')
txt.grid(row = 0, column = 0, sticky = 'NW')

text_status = tk.StringVar(value = 'Idle')
status_label = tk.Label(root, textvariable = text_status, fg = 'grey', font = 'Helvetica 10 bold', padx = 5)
status_label.grid(row = 0, column = 1, sticky = 'NW')





#TO DO
# #add menu
# my_menu = tk.Menu(root)
# root.config(menu = my_menu)

# #options
# options = tk.Menu(my_menu)
# my_menu.add_cascade(label = 'Options', menu = options)
# options.add_command(label = 'settings', command = str(), font = 'Helvetica 10')
# options.add_separator()
# options.add_command(label = 'credits', command = str(), font = 'Helvetica 10')





#start button
start_button = tk.Button(root, text = 'Force start', font = 'Helvetica 10 bold', width = 8, height = 4, command = lambda : start_miner())
start_button.place(x = 70, y = 60)
stop_button = tk.Button(root, text = 'Force stop', font = 'Helvetica 10 bold', width = 8, height = 4, command = lambda : stop_miner())
stop_button.place(x = 257, y = 60)


#progress time

def next_time_check():
    global wait_time_active
    global wait_time_inactive
    if started:
        if wait_time_active <= 0:
            wait_time_active = diz['wait_time_active']
            decide()
        else:
            wait_time_active -= 1
            d = timedelta(seconds = wait_time_active)
            time_check_label.config(text = d)
    if not started:
        if wait_time_inactive <= 0:
            wait_time_inactive = diz['wait_time_inactive']
            decide()
        else:
            wait_time_inactive -= 1
            d = timedelta(seconds = wait_time_inactive)
            time_check_label.config(text = d)
    time_check_label.after(1000, next_time_check)

#next check labels
next_check = tk.Label(root, text = 'Next check:', font = 'Helvetica 10 bold')
next_check.place(x = 0, y = 200)
time_check_label = tk.Label(root, text = '', font = 'Courier 16', fg = 'red')
time_check_label.place(x = 82, y = 196.7)

#api status labels
api_status = tk.Label(root, text = 'API status:', font = 'Helvetica 10', bg = 'light grey')
api_status.place(x = 240, y = 0)

text_connection = tk.StringVar(value = 'Waiting')
connection_attempt = tk.Label(root, textvariable = text_connection, fg = 'grey', font = 'Helvetica 10 bold')
connection_attempt.place(x = 315, y = 0)


#last gas value
last_recorded = tk.Label(root, text = 'Gas Value:', font = 'Helvetica 10', bg = 'light grey')
last_recorded.place(x = 5, y = 221)

text_gas = tk.StringVar(value = '')
gas_label = tk.Label(root, textvariable = text_gas, font = 'Helvetica 10 bold')
gas_label.place(x = 82, y = 221)




next_time_check()
check_process_running()


root.mainloop()
