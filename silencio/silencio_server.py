""" 
Silencio-Server
2017-07-13

Created By:
Avery Dodd
Aaron Moen
Omnielle Halton
Nolan LeWarne

Created for:
Seng 299 Summer 2017
"""

from server.server_network import network
from server.server_database import database


if __name__ == "__main__":
    base = database()
    net = network(7700)

    while True:
        net.listen()
