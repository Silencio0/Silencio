import sys
import socket
import datetime
from .client_message import message
from .client_message_table import message_table

class network(object):
    """This class is designed to handle network message sending and recieving for the client end"""

    def __init__(self, server_addr, server_port):
        """ Default constructor for client network. Requires the server address and port number as inputs. Returns false if connection fails."""

        local_addr = ('localhost', 7700)
        server_socket = (server_addr, server_port)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection = socket.bind(local_addr)
        
        try:
            connection.create_connect(server_port)

        except:
            print >> sys.stderr, 'failed to connect to server \n'
            failed = True
            connection.close()
            return False

    def __init__(self, server_addr, server_port, local_port):
        """ Constructor for client network. Requires the server address, server port, and local port as inputs. Returns false if connection fails."""

        local_addr = ('localhost', local_port)
        server_socket = (server_addr, server_port)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection = socket.bind(local_addr)
        
        try:
            connection.create_connect(server_port)

        except:
            print >> sys.stderr, 'failed to connect to server \n'
            failed = True
            connection.close()
            return False
        
    def login(input_user, input_pass):
        """ Function to send the login message to the server. Returns false if incorrect, True if correct. """
        #login and stuff

    def register(input_user, input_pass):
        """ Function to send a register message to the server. Returns false if cannot be registered, True if registered. """
        #register and login and stuff

    def listen():
        """ Function that checks the network port for incoming message and availability. Creates new messages for incoming messages. Appends incoming messages to message table. """
        #check if there's messages and stuff

    def send_message(input_message):
        """ Function that sends messages to the server. Calls listen first to make sure port is free. Returns false if it Fails, true otherwise. """
        #Send a message and stuff

    def disconnect():
        """ Function that disconnects client form the server. Returns True after successful disconnect."""
        #disconnect and stuff