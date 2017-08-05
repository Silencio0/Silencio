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


if __name__ == "__main__":
    
    interf = interface()

    while True:
        connected = interf.user_connect()

        if connected:
            break
    
    while True:
        logged = interf.user_login()

        if logged:
            break

    while True:

        worked = interf.user_listen() 

        if not worked:
            print('Connection failed. Exiting client.\n')
            break 

    