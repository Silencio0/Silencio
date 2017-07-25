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

from client.client_interface import interface
from client.client_network import network



if __name__ == "__main__":
    server_ip = 'localhost'
    serverport = 7600
    username = 'wat'
    password = 'pass'




    net = network(server_ip, server_port)
    interf = interface()

    if not net:
        print('Failed to connect to server\n')
    

    interf.user_login()

    while True:

        interf.user_listen()    

        out = net.listen()
        if out is not True and out is not False and out is not []:
            print(out)
    