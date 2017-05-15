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
from time import sleep
from matplotlib import pyplot as plt

#filename = '/home/inilabs/Desktop/Monaco_Roborace/03460001/caerOut-2017_05_12_16_36_40.aedat'
filename = '/home/inilabs/Desktop/Monaco_Roborace/02460003/caerOut-2017_05_12_16_39_38.aedat'
#filename = '/home/inilabs/Desktop/Monaco_Roborace/02460027/caerOut-2017_05_12_16_37_30.aedat'
#filename = '/home/inilabs/Desktop/Monaco_Roborace/02460046/caerOut-2017_05_12_16_36_21.aedat'
#filename = '/home/inilabs/Desktop/Monaco_Roborace/02460040/caerOut-2017_05_12_16_36_22.aedat'
file_read = open(filename, "rb")
xdim = 240
ydim = 180
NUMEVENTS = 6000

def matrix_active(x, y, pol):
    matrix = np.zeros([ydim, xdim])
    if(len(x) == len(y)):
        for i in range(len(x)):
            matrix[y[i], x[i]] = matrix[y[i], x[i]] +  pol[i] - 0.5  # matrix[x[i],y[i]] + pol[i]
    else:
        print("error x,y missmatch")
    return matrix

def sub2ind(array_shape, rows, cols):
    ind = rows * array_shape[1] + cols
    ind[ind < 0] = -1
    ind[ind >= array_shape[0] * array_shape[1]] = -1
    return ind

def ind2sub(array_shape, ind):
    ind[ind < 0] = -1
    ind[ind >= array_shape[0] * array_shape[1]] = -1
    rows = (ind.astype('int') / array_shape[1])
    cols = ind % array_shape[1]
    return (rows, cols)

def skip_header():
    ''' skip header '''
    line = file_read.readline()
    while line.startswith("#"):
        if ( line == '#!END-HEADER\r\n'):
            break
        else:
            line = file_read.readline()
            
            
def doubleMADsfromMedian(y,thresh=3.5):
    # warning: this function does not check for NAs
    # nor does it address issues when 
    # more than 50% of your data have identical values
    m = np.median(y)
    abs_dev = np.abs(y - m)
    left_mad = np.median(abs_dev[y <= m])
    right_mad = np.median(abs_dev[y >= m])
    y_mad = left_mad * np.ones(len(y))
    y_mad[y > m] = right_mad
    modified_z_score = 0.6745 * abs_dev / y_mad
    modified_z_score[y == m] = 0
    return modified_z_score > thresh

def read_events():
    """ A simple function that read events from cAER tcp"""
    
    #raise Exception
    data = file_read.read(28)

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
    #print("next read "+str(next_read)+" eventype "+str(eventtype))
    data = file_read.read(next_read)    
    counter = 0  # eventnumber[0]
    #return arrays
    x_addr_tot = []
    y_addr_tot = []
    pol_tot = []
    ts_tot =[]
    spec_type_tot =[]
    spec_ts_tot = []
    bw_tot = []

    if(eventtype == 1):  # something is wrong as we set in the cAER to send only polarity events
        while(data[counter:counter + eventsize]):  # loop over all event packets
            aer_data = struct.unpack('I', data[counter:counter + 4])[0]
            timestamp = struct.unpack('I', data[counter + 4:counter + 8])[0]
            x_addr = (aer_data >> 17) & 0x00007FFF
            y_addr = (aer_data >> 2) & 0x00007FFF
            x_addr_tot.append(x_addr)
            y_addr_tot.append(y_addr)
            pol = (aer_data >> 1) & 0x00000001
            pol_tot.append(pol)
            ts_tot.append(timestamp)
            # print (timestamp, x_addr, y_addr, pol)
            counter = counter + eventsize
    elif(eventtype == 0):
        spec_type_tot =[]
        spec_ts_tot = []
        while(data[counter:counter + eventsize]):  # loop over all event packets
            special_data = struct.unpack('I', data[counter:counter + 4])[0]
            timestamp = struct.unpack('I', data[counter + 4:counter + 8])[0]
            spec_type = (special_data >> 1) & 0x0000007F
            spec_type_tot.append(spec_type)
            spec_ts_tot.append(timestamp)
            if(spec_type == 6 or spec_type == 7 or spec_type == 9 or spec_type == 10):
                print (timestamp, spec_type)
            counter = counter + eventsize  
    elif(eventtype == 2):
        y_lenght = struct.unpack('I', data[24:28])[0]
        x_lenght = struct.unpack('I', data[20:24])[0]
        img_head = np.fromstring(data[:36], dtype=np.uint32)
        img_data = np.fromstring(data[36:], dtype=np.uint16)
        #is_rgb = np.logical_and(img_head[0],3)
        bw = np.reshape((img_data),(y_lenght, x_lenght))
        bw_tot.append(bw)
    elif(eventtype == 3):
        a=0   
    else:
        print("eventype "+str(eventtype))      


    return np.array(x_addr_tot), np.array(y_addr_tot), np.array(pol_tot), np.array(ts_tot), np.array(spec_type_tot), np.array(spec_ts_tot), bw_tot

def run(doblit=True):
    """
    Display the simulation using matplotlib, optionally using blit for speed
    """

    fig, ax = plt.subplots(1, 2)
    fig.set_size_inches(12,7)
    #spikes
    #ax[0].set_aspect('equal')
    ax[0].set_xlim(0, xdim)
    ax[0].set_ylim(0, ydim)
    ax[0].hold(True)
    ax[0].xaxis.set_visible(False)
    ax[0].yaxis.set_visible(False)
    #hist
    #ax[1].set_xlim(0, 6000)
    #ax[1].set_ylim(0, 5000)
    #ax[1].hold(True)
    #frame
    #ax[1].set_aspect('equal')
    ax[1].set_xlim(0, xdim)
    ax[1].set_ylim(0, ydim)
    ax[1].hold(True)
    ax[1].xaxis.set_visible(False)
    ax[1].yaxis.set_visible(False)
    skip_header()
    x, y, p, ts_tot, sp_t, sp_ts, bw = read_events()

    this_m = matrix_active(x, y, p)

    plt.show(False)
    plt.draw()

    if doblit:
        # cache the background
        background = fig.canvas.copy_from_bbox(ax[0].bbox)
        backgrounda = fig.canvas.copy_from_bbox(ax[1].bbox)
        #backgroundb = fig.canvas.copy_from_bbox(ax[2].bbox) 

    this_m = this_m/np.max(this_m)
    points = ax[0].imshow(this_m, interpolation='nearest', cmap='binary', origin='upper')
    frames = ax[1].imshow(np.random.rand(xdim,ydim), interpolation='nearest', cmap='binary', origin='upper', extent=[0,xdim,0,ydim])
    hist_ts = np.zeros([2,100])
    #points_h = ax[1].plot(hist_ts[0,:], hist_ts[1,:], 'o')[0]
    tic = time.time()
    niter = 0
    slow_speed = 1.0

    x = np.array([])
    y = np.array([]) 
    p = np.array([])   
    ts_tot = np.array([])
    spec_type = np.array([])
    spec_type_ts = np.array([])
    bw_tot = np.array([])

    while(1):
        #sleep(slow_speed)
        # update the xy data
        x_t, y_t, p_t, ts_tot_t, spec_type_t, spec_type_ts_t, bw = read_events()
        if(np.size(bw)>1):
            bw_tot = bw
        #if((len(ts_tot_t) > 2) and (ts_tot_t[1] - ts_tot_t[::-1][0] < 10000)):
        if( (np.sum(len(x)) < NUMEVENTS) ):
            #print("keep accumulating "+str(np.sum(len(x))))
            x = np.append(x,x_t)
            y = np.append(y,y_t)
            p = np.append(p,p_t)
            ts_tot = np.append(ts_tot,ts_tot_t)
            spec_type_t = np.append(spec_type_t,spec_type_t)
            spec_type_ts = np.append(spec_type_ts,spec_type_ts_t)
        else:
            #print("draw "+str(np.sum(len(x))))
            if(len(ts_tot) > 2):
                time_window = np.max(ts_tot) - np.min(ts_tot)
                this_m = matrix_active(x.astype('int'),y.astype('int'),p.astype('int'))#[index_a], y
                hist_ts = np.zeros([2,100])
                aa, ba = np.histogram(np.diff(ts_tot),100)
                hist_ts[0,:] = ba[1::]
                hist_ts[1,:] = aa
                #raise Exception
                #points_h.set_data(hist_ts)
                points.set_data(np.flipud(this_m))
                if(np.size(bw_tot) > 0):
                    nframes = np.size(bw_tot)/(xdim*ydim)
                    frames.set_data((1.0 - (bw_tot[0]/65536.0)))
                    ax[1].autoscale_view(True,True,True)

                if doblit:
                    # restore background
                    fig.canvas.restore_region(background)

                    # redraw just the points
                    ax[0].draw_artist(points)
                    #ax[1].draw_artist(points_h)
                    if(np.size(bw_tot) > 0):
                        ax[1].draw_artist(frames) 

                    # fill in the axes rectangle
                    fig.canvas.blit(ax[0].bbox)
                    if(np.size(bw_tot) > 0):
                        fig.canvas.blit(ax[1].bbox)
                else:
                    # redraw everything
                    fig.canvas.draw()
                
                x = np.array([])
                y = np.array([]) 
                p = np.array([])   
                ts_tot = np.array([])
                spec_type = np.array([])
                spec_type_ts = np.array([])
                bw_tot = np.array([])



    plt.close(fig)

if __name__ == '__main__':
    run(doblit=True)
