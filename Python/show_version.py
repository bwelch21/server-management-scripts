import paramiko
from paramiko import client
import sys
import time

''' This script is intended to be used to run the "show version" command on a router/switch.                       
It opens an ssh connection to the remote device and executes said command. Hostname, Username,                    
and Password are all intended to be passed as command line arguments, respectively.'''

class ssh:
    client = None

    def __init__(self, address, username, password):
        print("Attempting to connect to the device...")
        # Create a new SSH client                                                                                 
        self.client = client.SSHClient()
        # Enables the script to be able to access a server that's not in the yet in the known_hosts file          
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        # Makes the connection to the given address with the username and password combo                          
        try:
            self.client.connect(address, username=username, password=password, look_for_keys=False)
            print("Connection to device opened successfully!")
        except:
            print("Unable to establish a connection to the device... Terminating.")
    def sendCommand(self, command):
        # Check if the connection was previously made                                                             
        if(self.client):
            stdin, stdout, stderr = self.client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                # Print data when available                                                                       
                if stdout.channel.recv_ready():
                    # Retrieves the first 1024 bytes that are sent to stdout                                      
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"
                    while prevdata:
                        # Retrieve the next 1024 bytes until there is nothing left                                
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata

                    # Print as a string                                                                           
                    print "Output of 'show version':\n"
                    print(str(alldata))
        else:
            print("Connection not opened.")

    def close(self):
        if(self.client):
            self.client.close()
            return True
        else: return False

host = sys.argv[1]
uname = sys.argv[2]
passwd = sys.argv[3]
print "Command(s) to be executed: 'show version'"
try:
    connection = ssh(host, uname, passwd)
except paramiko.ssh_exception.AuthenticationException:
    print "Authentication failed. Check your login credentials."

connection.sendCommand("show version")
time.sleep(2)
connection.close()