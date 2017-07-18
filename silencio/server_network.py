import socket
import sys
import datetime
import select
import re
from server_database import database
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
                        m = re.search(r"\[([A-Za-z0-9]+)\]", data)
                        if m:
                            in_brackets = m.group(1)
                        
                        data = data.split()
                        #seperate data by word
                        try:
                            #need this for /login username password
                            user_name = data[1]     
                            passkey = data[2]
                        except:
                            print("not enough arguments")

                        #performs command actions
                        if state == "/join":
                            join()
                        elif state == "/create":
                            create()
                        elif state == "/set_alias":
                            server_database.set_alias(in_brackets, username)
                        elif state == "/block":
                            block()
                        elif state == "/unblock":
                            unblock()
                        elif state == "/delete":
                            delete()
                        elif state == "/login":
                            if login(user_name, passkey) == 1:
                                print ("successfully logged on")
                        elif state == "/register":
                            register()
                        #I dont think this should be destroying data
                        #parseMessage returns 'message' if keywords aren't found
                        #so the message should be broadcasted here
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
    
    def login(self, user_name, passkey):
        """ Login function returns 1 if Username/Password match otherwise 0 """
        try:
            #poll database for user ifo
            userinfo = server_database.query_name(user_name)
            if userinfo[1] == passkey:
                return True
            else:
                sys.stderr.write("Incorrect password querry\n")
                return False
        except:
            #query_name couldn't find username, error message already in that function
            #try / except is here to avoid crashing when username is incorrect
            print("\n")
            return False

    def register(self, in_user, user_name, passkey):
        """ Register function returns true if successfully registered otherwise false """
        #store desired username and password in temp user, default alias to username
        to_register = stored_user(user_name, passkey, user_name)                            ####The idea was to only talk to database, not the stored user class!####
        if server_database.insert(to_register) == 1:
            sys.stderr.write ("Successfully registered with username: " + user_name
             + " to set an alias type /set_alias")
            in_user.username = user_name
            in_user.alias = user_name

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
            sys.stderr.write('Failed to broadcast message to non-existant room ' + in_room_name + '.\n')
            return False

        #send message to all users in the room
        else:
            sys.stderr.write('Broadcasting message to chat room named ' + in_room_name + '.\n')
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
        
        port = in_user.assigned_port

        #check if message is blocked
        blocked = database.retrieve_blocked_users(in_user.username)
        if in_message.sender in blocked:
            return False

        #if not, send message
        else:
            port.send("\r" + '[' + str(in_message.sender.get_alias()) + ' : ' + str(in_message.timestamp) + ']'
             + in_message.string)
            return True

    def send_server_feedback(self, in_user, in_string):
        """ Function to send a message to a specific user to provide feedback on their action. ie moved to room or set alias, etc. """
        port = in_user.assigned_port
        port.send("\r" + '[SERVER : ' + datetime.now() + ']' + in_string)

    def create_chatroom(self, in_name, owning_user):
        """ Function to add an active chatroom """
    
        #check if name taken
        for room in self.active_chatroom_list:
            if room.name is in_name:
                sys.stderr.write('Failed to create chatroom named ' + in_name + '.\n')
                return False

        #create and return room
        newroom = active_chatroom(in_name, owning_user)
        self.active_chatroom_list.append(newroom)
        self.num_active_chatrooms += 1

        sys.stderr.write('Succesfully created chatroom named ' + in_name + '.\n')

    def destroy_chatroom(self, in_name):
        """ Function to remove an active chatroom. Looks up chatroom by name and removes it. Returns true if successful, false if not found. """
        
        #find default room to send users to
        for room in self.num_active_chatrooms:
            if room.name is 'default':    
                default = room

        #find room and remove it
        for room in self.active_chatroom_list:
                       
            if room.name is in_name:

                #empty users into default room
            for user in room.users:
                user.current_room = default

                self.active_chatroom_list.remove(room)
                self.num_active_cahtrooms -= 1
                sys.stderr.write('Successfully destroyed chat room named ' + in_name + '.\n')
                return True

        #room not found
        sys.stderr.write('Failed to destroy chatroom named ' + in_name + ' as it was not found.\n')
        return false