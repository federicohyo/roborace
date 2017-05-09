#!/usr/bin/env python

######################################
# REAL TIME EVENT DISPLAY FROM cAER
# ONLY POLARITY make sure you change
# PARAMETERS according to your setup
# author federico.corradi@inilabs.com
######################################

import socket
import struct
import numpy as np
import time
import matplotlib
#matplotlib.use('GTKAgg')
from matplotlib import pyplot as plt
from matplotlib import animation

# PARAMETERS
host = "192.168.42.9"
port = 7777

sock = socket.socket()
sock.connect((host, port))

## as in http://inilabs.com/support/software/fileformat/#h.kbta1pm6k3qt
data = sock.recv(20, socket.MSG_WAITALL)
network = struct.unpack("<Q", data[0:8])[0]
sequence_number = struct.unpack("<Q", data[8:16])[0]
aedat_ver = struct.unpack("B", data[16])[0]
format_number = struct.unpack("B", data[17])[0]
source_number = struct.unpack("H", data[18:20])[0]
if(network != 2105305046418351704):
    print("Error in network please retry")
    raise Exception
if(sequence_number != 0 ):
    print("Error in network please retry, sequence number not zero.")
    raise Exception        
if(aedat_ver != 1):
    print("Aedat version not implemented -> " + str(aedat_ver))
    raise Exception                 
if(format_number != 0 ):   
    print("Format Number version not implemented -> " + str(format_number))
    raise Exception   
if(source_number != 20 ):
    print("Source Number not imagegenerator - roborace - not implemented " + str(source_number))
    raise Exception


data = sock.recv(28, socket.MSG_WAITALL)  # we read the header of the packet

# read header
eventtype = struct.unpack('H', data[0:2])[0]
eventsource = struct.unpack('H', data[2:4])[0]
eventsize = struct.unpack('I', data[4:8])[0]
eventoffset = struct.unpack('I', data[8:12])[0]
eventtsoverflow = struct.unpack('I', data[12:16])[0]
eventcapacity = struct.unpack('I', data[16:20])[0]
eventnumber = struct.unpack('I', data[20:24])[0]
eventvalid = struct.unpack('I', data[24:28])[0]
next_read = eventcapacity * eventsize  # we now read the full packet
data = sock.recv(next_read, socket.MSG_WAITALL) 

# frame event type
if(eventtype == 2):
    y_lenght = struct.unpack('I', data[24:28])[0]
    x_lenght = struct.unpack('I', data[20:24])[0]
    img_head = np.fromstring(data[:36], dtype=np.uint32)
    img_data = np.fromstring(data[36:], dtype=np.uint16)
    is_rgb = np.logical_and(img_head[0],3)
    if(is_rgb):
        col = np.reshape(img_data,(x_lenght, y_lenght,3))
    else:
        bw = np.reshape(img_data,(x_lenght, y_lenght))

nx = y_lenght
ny = x_lenght
fig = plt.figure(figsize=(6, 4), dpi=80, facecolor='w', edgecolor='k')
data = np.zeros((nx, ny, 3))
plt.title(host)
im = plt.imshow(data, cmap='copper', vmin=0, vmax=1)
plt.axis('off')
plt.ion()
plt.show()

def init():
    im.set_data(np.zeros((nx, ny)))

def animate(i):
    data = sock.recv(28, socket.MSG_WAITALL)  # we read the header of the packet

    # read header
    eventtype = struct.unpack('H', data[0:2])[0]
    eventsource = struct.unpack('H', data[2:4])[0]
    eventsize = struct.unpack('I', data[4:8])[0]
    eventoffset = struct.unpack('I', data[8:12])[0]
    eventtsoverflow = struct.unpack('I', data[12:16])[0]
    eventcapacity = struct.unpack('I', data[16:20])[0]
    eventnumber = struct.unpack('I', data[20:24])[0]
    eventvalid = struct.unpack('I', data[24:28])[0]
    next_read = eventcapacity * eventsize  # we now read the full packet
    data = sock.recv(next_read, socket.MSG_WAITALL) 

    # frame event type
    if(eventtype == 2):
        y_lenght = struct.unpack('I', data[24:28])[0]
        x_lenght = struct.unpack('I', data[20:24])[0]
        img_head = np.fromstring(data[:36], dtype=np.uint32)
        img_data = np.fromstring(data[36:], dtype=np.uint16)
        is_rgb = np.logical_and(img_head[0],3)
        if(is_rgb):
            col = np.reshape(img_data,(x_lenght, y_lenght,3))
        else:
            bw = np.reshape(img_data,(x_lenght, y_lenght))

    im.set_data(col)
    return im

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=nx * ny,
                               interval=50)






