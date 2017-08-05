import sys
import socket
import datetime
import select



class network(object):
    """This class is designed to handle network message sending and recieving for the client end"""

    def __init__(self, server_addr, server_port):
        """ Default constructor for client network. Requires the server address and port number as inputs. Returns false if connection fails."""

    def __init__(self, server_addr, server_port, local_port):
        """ Constructor for client network. Requires the server address, server port, and local port as inputs. Returns false if connection fails."""

        if local_port is None:
            self.local_addr = ('localhost', 7700) 
        else:
            self.local_addr = ('localhost', local_port)
        self.server_socket = (server_addr, server_port)
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = socket.bind(self.local_addr)
        self.message_q = []
        
        try:
            self.connection.create_connect(server_port)

        except:
            sys.stderr.write('failed to connect to server \n')
            failed = True
            self.connection.close()
            return False
        
    def login(self, input_user, input_pass):
        """ Function to send the login message to the server. Returns false if incorrect, True if correct. """
        try:
            self.send_message('/login [' + input_user + '] [' + input_pass + ']\r')

        except:
            sys.stderr.write('failed to login to server. \n') 
            return False

        return True

    def register(input_user, input_pass):
        """ Function to send a register message to the server. Returns false if cannot be registered, True if registered. """
        try:
            self.send_message('/register [' + input_user + '] [' + input_pass + ']\r')

        except: 
            return False
            sys.stderr.write('failed to register with server. \n')

        return True

    def listen(self):
        """ Function that checks the network port for incoming message and availability. Creates new messages for incoming messages. Appends incoming messages to message table. """
        readable, writeable, errored = select.select(self.connection)
        
        if self.connection in readable:
            text = self.read_connection()
            return text

        if self.connection in writeable:
            for message in self.message_q:

                #attempt message send.
                sent = self.send_message(message)

                if not sent:
                    return False
                    
                self.message_q.remove(message)
            
            return True

        if self.connection in errored:

            self.disconnect()
            return 'Connection errored out'

        return False

    def send_message(self,input_message):
        """ Function that sends messages to the server. Calls listen first to make sure port is free. Returns false if it Fails, true otherwise. """
        try: 
            self.connection.send('\r' + input_message + '\r')

        except:
            sys.stderr.write('failed to send message to server \n') 
            return False

        return True

    def read_connection (self):
        sock = self.connection
        string = sock.recv(4098)

        return string

    def disconnect(self):
        """ Function that disconnects client form the server. Returns True after successful disconnect."""
        self.connection.close()

    def q_send(send, in_string):
        """ Function for appending a message to the message queue """
        self.message_q.append(in_string)