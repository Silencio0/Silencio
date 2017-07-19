""" 
Silencio-Client
2017-07-13

Created By:
Avery Dodd
Aaron Moen
Omnielle Halton
Nolan LeWarne

Created for:
Seng 299 Summer 2017
"""

from .client_interface import interface
from .client_network import network

server_ip = 'localhost'
serverport = 7600
username = 'wat'
password = 'pass'




net = network(server_ip, server_port)

if not net:
    print('Failed to connect to server\n')
    

if net.login(username, password):
    print ('Successfully logged in\n')
else:
    print ('failed to log in\n')

while True:
    out = net.listen()
    if out is not True and out is not False and out is not []:
        print(out)
    