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

from .server_network import network
from .server_database import database

base = database()
net = network('localhost')

while True:
    net.listen()
