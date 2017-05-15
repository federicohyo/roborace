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
import file_parser

#filename = '/home/federico/NAS/DVS big data/Monaco_Roborace/03460001/caerOut-2017_05_12_16_36_40.aedat'
#filename = '/home/federico/NAS/DVS big data/Monaco_Roborace/02460003/caerOut-2017_05_12_16_39_38.aedat'
#filename = '/home/federico/NAS/DVS big data/Monaco_Roborace/02460027/caerOut-2017_05_12_16_37_30.aedat'
#filename = '/home/federico/NAS/DVS big data/Monaco_Roborace/02460046/caerOut-2017_05_12_16_36_21.aedat'

NUMEVENTS = 3000

filenames = ['/home/federico/NAS/DVS big data/Monaco_Roborace/02460040/caerOut-2017_05_12_16_36_22.aedat',
             '/home/federico/NAS/DVS big data/Monaco_Roborace/02460046/caerOut-2017_05_12_16_36_21.aedat'] 
             #'/home/federico/NAS/DVS big data/Monaco_Roborace/02460027/caerOut-2017_05_12_16_37_30.aedat',
             #'/home/federico/NAS/DVS big data/Monaco_Roborace/02460015/caerOut-2017_05_12_16_37_31.aedat',
             #'/home/federico/NAS/DVS big data/Monaco_Roborace/02460003/caerOut-2017_05_12_16_39_38.aedat',
             #'/home/federico/NAS/DVS big data/Monaco_Roborace/02460003/caerOut-2017_05_12_16_39_38.aedat']

pa = [file_parser.file_parser(xdim=240, ydim=180, filename=filenames[i]) for i in range(len(filenames))]

def run(doblit=True):
    """
    Display the simulation using matplotlib, optionally using blit for speed
    """

    n_cameras = len(pa)

    x = [None]*n_cameras  
    y = [None]*n_cameras  
    p = [None]*n_cameras  
    ts_tot = [None]*n_cameras  
    sp_t = [None]*n_cameras  
    sp_ts = [None]*n_cameras  
    bw = [None]*n_cameras  
    background = [[None]*n_cameras, [None]*n_cameras]
    this_m = [None]*n_cameras
    points =  [None]*n_cameras
    frames = [None]*n_cameras
    
    for i in range(n_cameras):
        pa[i].skip_header()
        x[i], y[i], p[i], ts_tot[i], sp_t[i], sp_ts[i], bw[i] = pa[i].read_events()

    fig, ax = plt.subplots(2, n_cameras)
    fig.set_size_inches(12*n_cameras,7*n_cameras)
    for i in range(n_cameras):
        #spikes 
        ax[0][i].set_xlim(0, pa[i].xdim)
        ax[0][i].set_ylim(0, pa[i].ydim)
        ax[0][i].hold(True)
        ax[0][i].xaxis.set_visible(False)
        ax[0][i].yaxis.set_visible(False)
        #frames 
        ax[1][i].set_xlim(0, pa[i].xdim)
        ax[1][i].set_ylim(0, pa[i].ydim)
        ax[1][i].hold(True)
        ax[1][i].xaxis.set_visible(False)
        ax[1][i].yaxis.set_visible(False)
    
        if doblit:
            # cache the background
            background[i][0] = fig.canvas.copy_from_bbox(ax[0][i].bbox)
            background[i][1] = fig.canvas.copy_from_bbox(ax[1][i].bbox)

        this_m[i] = pa[i].matrix_active(x[i], y[i], p[i])
   
        fig.show(False)
        plt.draw()

        this_m[i] = this_m[i]/np.max(this_m[i])
        points[i] = ax[0][i].imshow(np.random.rand(pa[i].xdim,pa[i].ydim), interpolation='nearest', cmap='binary', origin='upper', extent=[0,pa[i].xdim,0,pa[i].ydim])
        frames[i] = ax[1][i].imshow(np.random.rand(pa[i].xdim,pa[i].ydim), interpolation='nearest', cmap='binary', origin='upper', extent=[0,pa[i].xdim,0,pa[i].ydim])

    x = [np.array([]) for i in range(n_cameras)]
    y = [np.array([]) for i in range(n_cameras)]
    p = [np.array([]) for i in range(n_cameras)]
    ts_tot = [np.array([]) for i in range(n_cameras)]
    spec_type = [np.array([]) for i in range(n_cameras)]
    spec_type_ts = [np.array([]) for i in range(n_cameras)]
    bw_tot = [np.array([]) for i in range(n_cameras)]

    while(1):
        for i in range(n_cameras):
            #sleep(slow_speed)
            x_t, y_t, p_t, ts_tot_t, spec_type_t, spec_type_ts_t, bw = pa[i].read_events()
            if(np.size(bw)>1):
                bw_tot[i] = bw
            #if((len(ts_tot_t) > 2) and (ts_tot_t[1] - ts_tot_t[::-1][0] < 10000)):
            if( (np.sum(len(x[i])) < NUMEVENTS) ):
                #print("keep accumulating "+str(np.sum(len(x[i]))))
                x[i] = np.append(x[i],x_t)
                y[i] = np.append(y[i],y_t)
                p[i] = np.append(p[i],p_t)
                ts_tot[i] = np.append(ts_tot[i],ts_tot_t)
                spec_type[i] = np.append(spec_type[i],spec_type_t)
                spec_type_ts[i] = np.append(spec_type_ts[i],spec_type_ts_t)
            else:
                #print("draw "+str(np.sum(len(x[i]))))
                if(len(ts_tot[i]) > 2):
                    time_window = np.max(ts_tot[i]) - np.min(ts_tot[i])
                    this_m[i] = pa[i].matrix_active(x[i].astype('int'),y[i].astype('int'),p[i].astype('int'))
                    points[i].set_data(this_m[i])
                    if(np.size(bw_tot[i]) > 0):
                        nframes = np.size(bw_tot)/(pa[i].xdim*pa[i].ydim)
                        frames[i].set_data((1.0 - (bw_tot[i][0]/65536.0)))
                        ax[1][i].autoscale_view(True,True,True)

                    if doblit:
                        # restore background
                        fig.canvas.restore_region(background[i][0])
                        fig.canvas.restore_region(background[i][1])

                        # redraw just the points
                        ax[0][i].draw_artist(points[i])
                        if(np.size(bw_tot) > 0):
                            ax[1][i].draw_artist(frames[i]) 

                        # fill in the axes rectangle
                        fig.canvas.blit(ax[0][i].bbox)
                        if(np.size(bw_tot) > 0):
                            fig.canvas.blit(ax[1][i].bbox)
                    else:
                        # redraw everything
                        fig.canvas.draw()
                    
                    x[i] = np.array([])
                    y[i] = np.array([]) 
                    p[i] = np.array([])   
                    ts_tot[i] = np.array([])
                    spec_type[i] = np.array([])
                    spec_type_ts[i] = np.array([])
                    bw_tot[i] = np.array([])

    plt.close(fig)

if __name__ == '__main__':
    run(doblit=False)
