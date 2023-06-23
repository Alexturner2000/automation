import paramiko
import time
import os
import configparser
import subprocess
import smtplib
from email.message import EmailMessage
from paramiko.ssh_exception import BadHostKeyException, AuthenticationException, SSHException
import socket

time.sleep(1)

def address_fetch():
        """
        Reads the ip addresses in the text document and saves them to a list

        Returns:
                device_ip_list (list): List of the IP addresses of devicees
        """

        with open('device_ip_list.txt', 'r+') as f:
                device_ip_list = f.readlines()
                if not device_ip_list:
                        print ("There are no addresses")
                        return None
        return device_ip_list


def network_device_fetch(device_ip, execute_command):
        """
        Connects to each network device and fetches the configuration
        

        Args:
            device_ips (list): List of the IP addresses of devicees
            execite_command (list): List of CLI commands sent to the network device

        Returns:
            None
        """
        
        for device_ip in device_ip:
                host = device_ip.strip()                        
                ssh_pre = paramiko.SSHClient()
                ssh_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                try:
                        ssh_pre.connect(host, username='admin', password='NiceTry')       
                        print("SSH connection established to " + host)
                        
                        ssh_post = ssh_pre.invoke_shell()
                        print("Interactive SSH session established")


                        ssh_post.send("enable\n")
                        
                        for execute_command in execute_command:
                                ssh_post.send(execute_command)
                                time.sleep(1000)

                        output_coded = ssh_post.recv(100000)
                        output = output_coded.decode('utf-8')

                        with open(f'/devicebackupscript/{host}/{host}.config', 'w+') as fp:
                                fp.write(output)

                except AuthenticationException:
                        print("Authentication failed, please verify your credentials: %s")

                except SSHException as sshException:
                        print("Unable to establish SSH connection: %s" % sshException)

                except socket.error as socketerr:
                        print("Socket error: %s" % socketerr)

                finally:
                        ssh_pre.close()


def main():
        # IP Address retrival
        device_ip_list = address_fetch()
        if device_ip_list is None:
                quit("No addresses") 
        
        execute_command = ("show run\n")
        network_device_fetch(device_ip_list, execute_command)
             

if __name__ == "__main__":
    main()






# Backup 
# ssh_post.send("terminal length 0\n")
# ssh_post.send("show version\n")
# ssh_post.send("show ip route\n")
# ssh_post.send("show interface status\n")
# ssh_post.send("show run\n")
# ssh_post.send("exit\n")