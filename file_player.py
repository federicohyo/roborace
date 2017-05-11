#program that runs caer with file inputs 
#support drag and drop for changing filepath
#
# author federico.corradi@gmail.com
import caer_communication
import psutil
import numpy as np
import os

ip_caer = '127.0.0.1'
port_ssh = 22
port = 4040
caer_start_file_input = '/media/federico/e247eb2e-273d-4a18-895a-6dd4c877d551/inilabs/caer/caer-bin-file-input'

#scripting part check caer status and start it
control = caer_communication.caer_communication(host=ip_caer)

is_caer_file_running = False
for pid in psutil.pids():
    p = psutil.Process(pid)
    if p.name() == "caer-bin-file-input":
        print("used caer:"+ str(p.cmdline()))
        is_caer_file_running = True
        
if(is_caer_file_running == False):        
    print("PLEASE START CAER-FILE-INPUT !")
    #os.system(caer_start_file_input)
else:
    print("CAER FILE INPUT RUNNING...")

if(control.open_communication_command() == False):
    print("PLEASE START CAER-FILE-INPUT... exiting now")
    raise Exception


import Tkinter
from untested_tkdnd_wrapper import TkDND

root = Tkinter.Tk()

dnd = TkDND(root)

entry_filea = Tkinter.Entry()
entry_filea.pack()

entry_fileb = Tkinter.Entry()
entry_fileb.pack()

global current_speed 
current_speed = 10000
global change_factor
change_factor = 20

def handlefilea(event):
    event.widget.insert(0, event.data)
    line = event.data.translate(None, '{}')
    print "Changing File Input 10"
    cmd = 'put /1/100-FileInput/ PacketContainerInterval int '+str(current_speed)
    control.send_command(cmd)
    cmd = 'put /1/10-FileInput/ filePath string '+line.strip()
    control.send_command(cmd)

def handlefileb(event):
    event.widget.insert(0, event.data)
    line = event.data.translate(None, '{}')
    print "Changing File Input 10"
    cmd = 'put /1/100-FileInput/ PacketContainerInterval int '+str(current_speed)
    control.send_command(cmd)
    cmd = 'put /1/100-FileInput/ filePath string '+line.strip()
    control.send_command(cmd)   
    
def faster():
    print "Changing Speed .. faster"
    current_speed  += int((current_speed/100)+change_factor)
    cmd = 'put /1/100-FileInput/ PacketContainerInterval int '+str(current_speed)
    control.send_command(cmd)   
    cmd = 'put /1/10-FileInput/ PacketContainerInterval int '+str(current_speed)
    control.send_command(cmd)   

def slower():
    print "pausing..."
    current_speed  -= int((current_speed/100)+change_factor)
    cmd = 'put /1/100-FileInput/ PacketContainerInterval int '+str(current_speed)
    control.send_command(cmd)   
    cmd = 'put /1/10-FileInput/ PacketContainerInterval int '+str(current_speed)
    control.send_command(cmd)  

def pause():
    print "Changing Speed .. slower"
    cmd = 'put /1/100-FileInput/ pause bool true'
    control.send_command(cmd)   
    cmd = 'put /1/10-FileInput/ pause bool true'
    control.send_command(cmd)   
    
def play():
    print "Changing Speed .. slower"
    cmd = 'put /1/100-FileInput/ pause bool false'
    control.send_command(cmd)   
    cmd = 'put /1/10-FileInput/ pause bool false'
    control.send_command(cmd) 
    cmd = 'put /1/10-FileInput/ running bool true'
    control.send_command(cmd)   
    cmd = 'put /1/100-FileInput/ running bool true'
    control.send_command(cmd)   


B = Tkinter.Button(root, text ="faster", command = faster)
B.pack()
B = Tkinter.Button(root, text ="slower", command = slower)
B.pack()
B = Tkinter.Button(root, text ="play", command = play)
B.pack()
B = Tkinter.Button(root, text ="pause", command = pause)
B.pack()

dnd.bindtarget(entry_filea, handlefilea, 'text/uri-list')
dnd.bindtarget(entry_fileb, handlefileb, 'text/uri-list')

root.mainloop()
