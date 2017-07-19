import sys
import socket
import datetime
import select



class network(object):
    """This class is designed to handle network message sending and recieving for the client end"""

    def __init__(self, server_addr, server_port):
        """ Default constructor for client network. Requires the server address and port number as inputs. Returns false if connection fails."""

        self.local_addr = ('localhost', 7700)
        self.server_socket = (server_addr, server_port)
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = socket.bind(self.local_addr)
        self.message_q = []
        
        try:
            self.connection.create_connect(server_port)

        except:
            sys.stderr.write('failed to connect to server \n')
            failed = True
            connection.close()
            return False

    def __init__(self, server_addr, server_port, local_port):
        """ Constructor for client network. Requires the server address, server port, and local port as inputs. Returns false if connection fails."""

        self.local_addr = ('localhost', local_port)
        self.server_socket = (server_addr, server_port)
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = socket.bind(self.local_addr)
        self.message_q = []
        
        try:
            connection.create_connect(server_port)

        except:
            sys.stderr.write('failed to connect to server \n')
            failed = True
            connection.close()
            return False
        
    def login(self, input_user, input_pass):
        """ Function to send the login message to the server. Returns false if incorrect, True if correct. """
        try:
            self.send_message('/login [' + input_user + '] [' + input_pass + ']\r')

        except: 
            return False

        return True

    def register(input_user, input_pass):
        """ Function to send a register message to the server. Returns false if cannot be registered, True if registered. """
        #register and login and stuff

    def listen(self):
        """ Function that checks the network port for incoming message and availability. Creates new messages for incoming messages. Appends incoming messages to message table. """
        readable, writeable, errored = select.select(self.connection)
        
        if self.connection in readable:
            text = self.read_connection()
            return text

        if self.connection in writeable:
            for message in self.message_q:
                send_message(message)
                sel.message_q.remove(message)
            
            return True

        if self.connection in errored:

            self.disconnect()
            return 'Connection errored out'

        return False

    def send_message(self,input_message):
        """ Function that sends messages to the server. Calls listen first to make sure port is free. Returns false if it Fails, true otherwise. """
        try: 
            connection.send('\r' + input_message + '\r')

        except:
            #message failed 
            return False

        return True

    def read_connection (self):
        sock = self.connection
        string = sock.recv(4098)

        return string

    def disconnect(self):
        """ Function that disconnects client form the server. Returns True after successful disconnect."""
        connection.close()

    def q_send(send, in_string):
        self.message_q.append(in_string)