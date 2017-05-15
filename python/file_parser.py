import numpy as np
import socket
import struct
import time

class file_parser:
    def __init__(self, xdim = 346, ydim = 260, filename=None):
        self.xdim = xdim
        self.ydim = ydim
        self.filename = filename
        self.file_read = open(self.filename, "rb")

    def matrix_active(self, x, y, pol):
        matrix = np.zeros([self.ydim, self.xdim])
        if(len(x) == len(y)):
	    for i in range(len(x)):
	        matrix[y[i], x[i]] = matrix[y[i], x[i]] +  pol[i] - 0.5  # matrix[x[i],y[i]] + pol[i]
        else:
	    print("error x,y missmatch")
        return matrix

    def sub2ind(self, array_shape, rows, cols):
        ind = rows * array_shape[1] + cols
        ind[ind < 0] = -1
        ind[ind >= array_shape[0] * array_shape[1]] = -1
        return ind

    def ind2sub(self, array_shape, ind):
        ind[ind < 0] = -1
        ind[ind >= array_shape[0] * array_shape[1]] = -1
        rows = (ind.astype('int') / array_shape[1])
        cols = ind % array_shape[1]
        return (rows, cols)

    def skip_header(self):
        ''' skip header '''
        line = self.file_read.readline()
        while line.startswith("#"):
	    if ( line == '#!END-HEADER\r\n'):
	        break
	    else:
	        line = self.file_read.readline()
	        
	        
    def doubleMADsfromMedian(self, y,thresh=3.5):
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

    def read_events(self):
        """ A simple function that read events from cAER tcp"""
        
        #raise Exception
        data = self.file_read.read(28)

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
        data = self.file_read.read(next_read)    
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

