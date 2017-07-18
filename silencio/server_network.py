import socket
import sys
import datetime
import select
from .server_active_user import active_user
from .server_active_chatroom import active_chatroom
from .server_message import message

class network(object):
    """Server network class that does all the hard stuff."""
    
    def __init__ (self):
        """ Default Network constructor"""

        # Create empty connection variables
        self.num_connections = 0
        self.connection_list
        self.num_active_users = 0
        self.active_user_list
        self.num_active_chatrooms = 0
        self.active_chatroom_list
        self.server_addr = ('localhost', 7700)

        # Ready initial connections port
        self.initial_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.initial_sock.bind(server_addr)
        self.initial_sock.listen()    
        
        #add initial connection port to connections for monitoring
        self.connection_list = [initial_sock]

        #init default chatroom
        admin = active_user('admin', 'NULL', 'localhost')
        default_room = self.create_chatroom(default, admin)

    def __init__ (self, server_addr):
        """ Network constructor with inputted server address formatted like ('localhost', 7700) """

        # Create empty connection variables
        self.num_connections = 0
        self.connection_list
        self.num_active_users = 0
        self.active_user_list
        self.num_active_chatrooms = 0
        self.active_chatroom_list

        # Ready initial connections port
        self.initial_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.initial_sock.bind(server_addr)
        self.initial_sock.listen()
        
        #add initial connection port to connections for monitoring
        self.connection_list = [initial_sock]

        #init default chatroom
        admin = active_user('admin', 'NULL', 'localhost')
        default_room = self.create_chatroom('default', admin)

    def listen (self):
        """function that listens to all connections for incoming traffic. Also listens to initial connection port. """ 
        readable, writeable, errored = select.select(self.connection_list, [],[])
        
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
                #receive data with buffer
                try:
                    data = self.recv_msg(s, 4096)
                    if data.string:
                        #message not empty
                        content = data
                        #determine what the message is for and perform that task
                        state = content.parse_message_type()
                        #finds the bracketed word, e.g /join [this] in_brackets = this
                        in_brackets = re.search(r"\[([A-Za-z0-9]+)\]", data)
                        if state == "/join":
                            join()
                        elif state == "/create":
                            create()
                        elif state == "/set_alias":
                            alias = in_brackets
                        elif state == "/block":
                            block()
                        elif state == "/unblock":
                            unblock()
                        elif state == "/delete":
                            delete()
                        else:
                            destroy_data()
                except:
                    print("no data recieved\n")

        for s in writeable:
            #handle writables
            dostuff()

        for s in errored:
            #handle socket errors
            dostuff()

    def broadcast(self, in_message, in_room_name):
        """ Broadcast function for bradcasting a message to a chatroom. Takes a message class and a room name string. Returns true if succeeds, false if room is not found."""
        
        #lookup chatroom
        room_found = False
        for room in active_chatroom_list:
            if room.name is in_room_name:
                room_found = True
                break

        #if chatroom does not exist, return false
        if room_found is False:
            return False

        #send message to all users in the room
        else:
            for user in room.users:
                if user is not in_message.sender:
                    send_msg(user, in_message)
                
        #record to chat log

        return True

    def recv_msg(self, sock, msglen):
        """ Function to recieve a message from a socket as seperate parts. Returns a message class """                
        data = sock.recv(msglen)

        for active_u in self.active_user_list:
            if active_u.assigned_port is sock:
                user = active_u.username
                chatroom = active_u.current_room
                break
            else:
                user = ' '
                chatroom = 0
        
        timestamp = str(datetime.now())

        text = str(data)
        
        newmessage = message(user, chatroom, text, timestamp)

        return newmessage
        
    def send_msg(self, in_user, in_message):
        """ Function to send a formatted message to a socket. Sends a tuple of (user, timestamp, text) as unformatted bytes. """
        in_user.assigned_port.send("\r" + '[' + str(in_message.sender.get_alias()) + ' : ' + str(in_message.timestamp) + ']' + in_message.string)

    def create_chatroom(self, in_name, owning_user):
        """ Function to add an active chatroom """
    
        #check if name taken
        for room in self.active_chatroom_list:
            if room.name is in_name:
                return False

        #create and return room
        newroom = active_chatroom(in_name, owning_user)
        self.active_chatroom_list.append(newroom)
        self.num_active_chatrooms += 1

    def destroy_chatroom(self, in_name):
        """ Function to remove an active chatroom. Looks up chatroom by name and removes it. Returns true if successful, false if not found. """

        #find room and remove it
        for room in self.active_chatroom_list:
            if room.name is in_name:
                self.active_chatroom_list.remove(room)
                self.num_active_cahtrooms -= 1
                return True

        #room not found
        return false