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

    interf.user_connect()
    
    interf.user_login()

    while True:

        interf.user_listen()    

    