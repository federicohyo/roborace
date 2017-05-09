from __future__ import division
import numpy as np
import caer_communication
import socket
import subprocess
import sys
import paramiko
from time import sleep

#settings
nbytes = 4096
port = 22
username = 'pi' 
password = 'inilabs'
caer_start = 'screen -d -m bash -c "/home/pi/inilabs/caer/caer-bin > /dev/null 2>&1";'
ip_zpi_master_synch = '192.168.42.1'
sn_cam_master_synch = '02460040'
ip_zpi_fx3 = '192.168.42.7'
fname = "cam_list.txt" #file containing lists of ips

#read file
with open(fname) as f:
    content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    ip_cams = [x.strip() for x in content] 

#find out alive ips 
alive_zpi = np.repeat(np.bool(False),len(ip_cams))
counter = 0 
for ip_cam in ip_cams:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3);
    try:
        s.connect((ip_cam, 22))
        print "%s Port 22 reachable" % ip_cam
        alive_zpi[counter] = True
    except socket.error as e:
        print "Error on connect: %s" % e
    s.close()

# init control class and open communication to all ip defined
control_stereo = [caer_communication.caer_communication(host=ip_cam) for ip_cam in ip_cams]

#attemp connection to all stereo pairs
#attemp to start cAER if not running
counter = 0
stereo_up = np.repeat(np.bool(False),len(ip_cams))
for current_ip in control_stereo:
    ret = control_stereo[counter].open_communication_command()
    if(ret == False):
        print "Couldnt connect with the socket-server for IP %s . stereo pair down\n" % ip_cams[counter] 
        print "Try to start cAER in the remote machine"
        #caer is off.. let's start it
        try:
            client = paramiko.Transport((ip_cams[counter], port))
            client.connect(username=username, password=password)
            stdout_data = []
            stderr_data = []
            session = client.open_channel(kind='session')
            session.exec_command(caer_start)
            while True:
                if session.recv_ready():
                    stdout_data.append(session.recv(nbytes))
                if session.recv_stderr_ready():
                    stderr_data.append(session.recv_stderr(nbytes))
                if session.exit_status_ready():
                    break
            print 'exit status: ', session.recv_exit_status()
            print ''.join(stdout_data)
            print ''.join(stderr_data)
            sleep(2)
            ret = current_ip.open_communication_command()
            if(ret == True):
                stereo_up[counter] = True
            session.close()
            client.close()
        except Exception:
            print 'host is down %s.. nothing to do\n' % ip_cams[counter]
    else:
        stereo_up[counter] = True
    counter += 1

#all rpi up and running
index_stereo = np.where(stereo_up)[0]
print "###############################################\n"
print "Connected with a total of %d cAER/rpi \n" % sum(stereo_up) 
for i in range(len(index_stereo)):
    print "cAER running in %s" % ip_cams[index_stereo[i]]
print "###############################################\n"

#only control the alive one
control_stereo = [caer_communication.caer_communication(host=ip_cams[index_stereo[i]]) for i in range(len(index_stereo))]
counter = 0;
for current_ip in control_stereo:
    control_stereo[counter].open_communication_command()
    counter+=1

#############################################
######## FUNCTION AVAILABLE IN THE SESSION
#############################################
def reset_timestamp():
    print "STEREO MASTER IS  %s sN: %s" % (ip_zpi_master_synch , sn_cam_master_synch)
    print "NOTE: THIS ASSUMES THAT THE MASTER CAMERA IS THE DEVICE NUMBER 1\n"
    counter=0
    for current_ctl in control_stereo:
        if(ip_cams[counter] == ip_zpi_master_synch):
            control_stereo[counter].send_command('put /1/1-DAVISFX2/DAVIS240C/multiplexer/ TimestampReset bool true')
            sleep(0.5)
            control_stereo[counter].send_command('put /1/1-DAVISFX2/DAVIS240C/multiplexer/ TimestampReset bool false')
        counter+=1

def check_synch_status():
    print "SYNC MASTER IS  %s sN: %s" % (ip_zpi_master_synch , sn_cam_master_synch)
    print "NOTE: THIS ASSUMES THAT THE MASTER CAMERA IS THE DEVICE NUMBER 1\n"
    counter=0
    for current_ctl in control_stereo:
        if(ip_cams[counter] == ip_zpi_master_synch):
            print "\n"
            print "THIS IS THE MASTER\n"
            control_stereo[counter].send_command('get /1/1-DAVISFX2/sourceInfo/ deviceIsMaster bool')
            control_stereo[counter].send_command('get /1/2-DAVISFX2/sourceInfo/ deviceIsMaster bool')
        elif(ip_cams[counter] == ip_zpi_fx3):
            control_stereo[counter].send_command('get /1/1-DAVISFX3/sourceInfo/ deviceIsMaster bool')
            control_stereo[counter].send_command('get /1/2-DAVISFX3/sourceInfo/ deviceIsMaster bool')
        else:
            control_stereo[counter].send_command('get /1/1-DAVISFX2/sourceInfo/ deviceIsMaster bool')
            control_stereo[counter].send_command('get /1/2-DAVISFX2/sourceInfo/ deviceIsMaster bool')
        counter+=1

def start_recordings():
    print "START RECORDINGS.."
    for current_ctl in control_stereo:
        current_ctl.send_command('put  /1/9-FileOutput/ running bool true')
        current_ctl.send_command('put  /1/99-FileOutput/ running bool true')

def stop_recordings():
    print "STOP RECORDINGS.."
    for current_ctl in control_stereo:
        current_ctl.send_command('put  /1/9-FileOutput/ running bool false')
        current_ctl.send_command('put  /1/99-FileOutput/ running bool false')

def check_file_status():
    print "CHECKING FILE STATUS FOR ALL STEREO UP"
    for i in range(len(index_stereo)):
        current_ip = ip_cams[index_stereo[i]]
        try:
            client = paramiko.Transport((current_ip, port))
            client.connect(username=username, password=password)
        except Exception:
            print 'host is down %s.. nothing to do\n' % ip_cams[index_stereo[i]]

        stdout_data = []
        stderr_data = []
        session = client.open_channel(kind='session')
        session.exec_command('ls -lah /home/pi/inilabs/data/*/*')
        while True:
            if session.recv_ready():
                stdout_data.append(session.recv(nbytes))
            if session.recv_stderr_ready():
                stderr_data.append(session.recv_stderr(nbytes))
            if session.exit_status_ready():
                break
        print 'exit status: ', session.recv_exit_status()
        print ''.join(stdout_data)
        print ''.join(stderr_data)
        session.close()
        client.close()

def killall_caers():
    print "STOPPING ALL CAER"
    for i in range(len(index_stereo)):
        #ip_cams[index_stereo[i]]
        print "Killing cAER in %s" % ip_cams[index_stereo[i]] 
        try:
            client = paramiko.Transport((ip_cams[index_stereo[i]], port))
            client.connect(username=username, password=password)
        except Exception:
            print 'host is down %s.. nothing to do\n' % ip_cams[index_stereo[i]]

        stdout_data = []
        stderr_data = []
        session = client.open_channel(kind='session')
        session.exec_command('pkill caer')
        while True:
            if session.recv_ready():
                stdout_data.append(session.recv(nbytes))
            if session.recv_stderr_ready():
                stderr_data.append(session.recv_stderr(nbytes))
            if session.exit_status_ready():
                break
        print 'exit status: ', session.recv_exit_status()
        print ''.join(stdout_data)
        print ''.join(stderr_data)
        print ".. Done\n"
        session.close()
        client.close()

def startall_caers():
    print "STARTING ALL CAER"
    for i in range(len(index_stereo)):
        #ip_cams[index_stereo[i]]
        print "Starting cAER in %s" % ip_cams[index_stereo[i]] 
        try:
            client = paramiko.Transport((ip_cams[index_stereo[i]], port))
            client.connect(username=username, password=password)
        except Exception:
            print 'host is down %s.. nothing to do\n' % ip_cams[index_stereo[i]]

        stdout_data = []
        stderr_data = []
        session = client.open_channel(kind='session')
        session.exec_command(caer_start)
        while True:
            if session.recv_ready():
                stdout_data.append(session.recv(nbytes))
            if session.recv_stderr_ready():
                stderr_data.append(session.recv_stderr(nbytes))
            if session.exit_status_ready():
                break
        print 'exit status: ', session.recv_exit_status()
        print ''.join(stdout_data)
        print ''.join(stderr_data)
        print ".. Done\n"
        session.close()
        client.close()


### reset timestamp and start all recordings by default

## GUI
import Tkinter
#import tkMessageBox
top = Tkinter.Tk()

#def helloCallBack():
#   tkMessageBox.showinfo( "Hello Python", "Hello World")

B = Tkinter.Button(top, text ="Start Recording", command = start_recordings)
B.pack()
B = Tkinter.Button(top, text ="Stop Recording", command = stop_recordings)
B.pack()
B = Tkinter.Button(top, text ="Check File Status", command = check_file_status)
B.pack()
B = Tkinter.Button(top, text ="Reset Timestamp", command = reset_timestamp)
B.pack()
B = Tkinter.Button(top, text ="Killall cAER", command = killall_caers)
B.pack()
B = Tkinter.Button(top, text ="StartAll cAER", command = startall_caers)
B.pack()
B = Tkinter.Button(top, text ="Check Synchronization", command = check_synch_status)
B.pack()

top.mainloop()
