import socket
import fcntl
import struct
from ftplib import FTP

def get_ip_address(ifname):
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0X8915,struct.pack('256s',ifname[:15]))[20:24])


def ftp_connect():
    ftp_server = '127.0.0.1'
    username = 'uftp'
    password = 'ftpd'
    ftp=FTP()
    ftp.set_debuglevel(2)
    ftp.connect(ftp_server,21) #connect
    ftp.login(username,password) #login
    return ftp

def ftp_download(remotepath,savename):
    print ftp.getwelcome() #show ftp information
    bufsize = 1024
    ftp=ftp_connect()
    localpath = './data/'+savename
    fp = open(localpath,'wb') #open file in read mode
    ftp.retrbinary('RETR ' + remotepath,fp.write,bufsize) #dowonload ftp file
    ftp.set_debuglevel(0) #close debug
    ftp.close()
    ftp.quit()
