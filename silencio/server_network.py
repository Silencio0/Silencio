import socket
import sys
import datetime
import select
from .server_active_user import active_user
from .server_active_chatroom import active_chatroom

class network(object):
    """Server network class that does all the hard stuff."""
    
    def __init__ (self):
        """ Default Network constructor"""

        # Create empty connection variables
        num_connections = 0
        connection_list
        num_active_users = 0
        active_user_list
        num_active_chatrooms = 0
        active_chatroom_list
        server_addr = ('localhost', 7700)

        # Ready initial connections port
        initial_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        initial_sock.bind(server_addr)
        initial_sock.listen()    
        
        #add initial connection port to connections for monitoring
        connection_list = [initial_sock]

    def __init__ (self, server_addr):
        """ Network constructor with inputted server address formatted like ('localhost', 7700) """

        # Create empty connection variables
        num_connections = 0
        connection_list
        num_active_users = 0
        active_user_list
        num_active_chatrooms = 0
        active_chatroom_list

        # Ready initial connections port
        initial_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        initial_sock.bind(server_addr)
        initial_sock.listen()
        
        #add initial connection port to connections for monitoring
        connection_list = [initial_sock]

    def listen (self):
        """function that listens to all connections for incoming traffic. Also listens to initial connection port. """ 
        readable, writeable, errored = select.select(connection_list, [],[])
        
        #for all readable ports in the list with connections waiting
        for s in readable:

            #if initial port has a connection waiting
            if s is initial_sock:

                #accept connection and add active user with no current username
                client_socket, address = initial_sock.accept()
                connection_list.append(client_socket)
                num_connections += 1
                new_user = active_user(client_socket, address)
                active_user_list.append(new_user)
                num_active_users +=1
            
            #else we read message from the socket
            else:
                domessagestuff()

                
                
                

        