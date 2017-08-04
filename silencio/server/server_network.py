import socket
import sys
import datetime
import select
import re
from server.server_database import database
from server.server_stored_user import stored_user
from server.server_active_user import active_user
from server.server_active_chatroom import active_chatroom
from server.server_message import message

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
        self.connection_list.append(initial_sock)

        #init default chatroom
        admin = active_user('admin', 'NULL', 'localhost')
        self.default_room = self.create_chatroom(default, admin)

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
        self.connection_list.append(initial_sock)

        #init default chatroom
        admin = active_user('admin', 'NULL', 'localhost')
        self.default_room = self.create_chatroom('default', admin)

    def listen (self):
        """function that listens to all connections for incoming traffic. Also listens to initial connection port. """ 
        readable, writeable, errored = select.select(self.connection_list, [],[])
        
        #for all readable ports in the list with connections waiting
        for s in readable:

            #if initial port has a connection waiting
            if s is initial_sock:

                #accept connection and add active user with no current username
                client_socket, address = initial_sock.accept()
                self.connection_list.append(client_socket)
                self.num_connections += 1
                new_user = active_user(client_socket, address)
                self.active_user_list.append(new_user)
                self.num_active_users +=1
            
            #else we read message from the socket and handle accordingly
            else:
                  
                try:
                    #recieve message and find metadata classes
                    incoming = self.recv_msg(s, 4096)
                    sent_by = incoming.sender
                    text = incoming.string
                    sent_in = incoming.sent_in                    
                    
                    #If message not empty
                    if text:
                        #determine what the message is for and perform that task
                        state = incoming.parse_message_type()
                        #finds the bracketed word, e.g /join [this] in_brackets = this
                        args = re.search(r"\[([A-Za-z0-9]+)\]", text)
                        if args:
                            in_brackets = args.group(1)
                        
                        
                        text = text.split()
                        #seperate data by word
                        

                        #join room command handling - fixed
                        if state == "/join":
                            
                            #if arguments exist
                            if args:
                                
                                #find room that matches argument
                                join_room = False
                                for room in self.active_chatroom_list:
                                    if room.name is in_brackets:
                                        join_room = room
                            
                                #if room cannot be found
                                if join_room == False:
                                    send_server_feedback(sent_by, "No room with that name can be found.\n")

                                #if forbidden room
                                elif join_room == 0:
                                    send_server_feedback(sent_by, "That room is not for you.\n")
                                
                                #else, move user to room
                                else:
                                    sent_in.users.remove(sent_by)
                                    sent_by.current_room = join_room
                                    join_room.users.append(sent_by)
                                    send_server_feedback(sent_by, 'Joined room.\n')
           
                            #if no arguments found
                            else:
                                send_server_feedback(sent_by, 'Please retry command and include arguments in the form /join [roomname]\n')
                            
                        #create room command handling - fixed
                        elif state == "/create":

                            #If arguments exist
                            if args:

                                #Check if name taken
                                desired_name = in_brackets
                                name_taken = False
                                for room in self.active_chatroom_list:
                                    if room.name == desired_name:
                                        name_taken = True
                                
                                #If name is taken
                                if name_taken or desired_name is 'default' or desired_name is '0':
                                    send_server_feedback(sent_by, 'Room already exists with that name.')
                                
                                #Else create room with vacant name
                                else:
                                    create_chatroom(in_brackets, sent_by)
                                    send_server_feedback(sent_by, 'Room created.\n')

                            #If no arguments found
                            else:
                                send_server_feedback(sent_by, 'Please try command again with room name in brackets. ie /create [roomname].\n')
                            
                        #set alias command handling - fixed
                        elif state == "/set_alias":

                            #if arguments exist
                            if args:

                                #if alias is outlawed
                                banned_names = ('admin', 'administrator', '', ' ', 'default', 'server', 'SERVER', '\n', '\r')
                                if in_brackets in banned_names:
                                    (sent_by, 'Cannot set alias to that name.\n')

                                #Alias allowed and set
                                else:
                                    sent_by.alias = in_brackets
                                    database.set_alias(in_brackets, username)
                                    sent_by.check_alias()

                            #if no args
                            else:
                                send_server_feedback(sent_by, 'Please try command again with desired alias in brackets. ie /set_alias [pseudonym].\n')

                        #block user command handling
                        elif state == "/block":
                            if database.retrieve_blocked_user(active_user, in_brackets) == True:
                                send_server_feedback(active_user, "Blocked " + in_brackets)
                            else:
                                send_server_feedback(active_user, "Could not block " + in_brackets)

                        #unblock user command handling
                        elif state == "/unblock":
                            if database.unblock_user(active_user, in_brackets) == True:
                                send_server_feedback(active_user, "Unblocked " + in_brackets)
                            else:
                                send_server_feedback(active_user, in_brackets + " is not blocked")

                        #delete room command handling
                        elif state == "/delete":
                            if sent_by == in_brackets.owner:
                                if destroy_chatroom(in_brackets) == True:
                                    send_server_feedback(active_user, "Destroyed chatroom: " + in_brackets)
                            else:
                                self.send_server_feedback(active_user, "Chatroom: " + in_brackets + 
                                " could not be destroyed. Either the chatroom doesn't exist or you are not the owner.")

                        #login user command handling
                        elif state == "/login":

                            #try to find needed args
                            try:
                                failed = False
                                user_name = args.group(1)     
                                passkey = args.group(2)

                            except:
                                self.send_server_feedback(sent_by, "not enough login information.  Try /login [username] [password]\n")
                                failed = True

                            #If login succeeds
                            if not failed and login(user_name, passkey) is True:

                                #set active user to have username and be in a room
                                sent_by.username = user_name
                                sent_by.current_room = self.default_room
                                self.default_room.users.append(sent_by)
                                send_server_feedback(sent_by, 'Successfully logged in.\n')

                            #if login fails
                            elif not failed:
                                self.send_user_feedback(sent_by, 'Failed to log in. Incorrect username and/or password')

                        #register user command handling
                        elif state == "/register":

                            #find command arguments
                            try:
                                failed = False
                                user_name = args.group(1)     
                                passkey = args.group(2)
                            except:
                                self.send_server_feedback(sent_by, "not enough login information.  Try /register [username] [password]\n")
                                failed = True

                            if not failed and len(user_name) < 16 and len(passkey) < 16 :
                                self.register(sent_by, user_name, passkey)
                                

                            else:
                                self.send_server_feedback(sent_by, 'Unable to register account with those parameters. Username and password must both be less than 16 characters\n')
                        
                        #Else we broadcast regular message
                        else:
                            broadcast(data, data.sent_in)
                            
                except:
                    sys.stderr.write("no data recieved\n")
                    return False
        
        #For all writeable ports, send messages if waiting.
        for s in writeable:
            #handle writables
            dos_nothing = True

        #For all errored ports, remove them if they have an associated user.
        for s in errored:
            #handle socket errors

            #attempt to associate port with a user
            errored_user = False
            for active_u in self.active_user_list:
                if active_u.assigned_port is s:
                    errored_user = active_u

            #if we can associate the port with a user, disconnect them
            if errored_user:

                #if port not yet logged in
                if errored_user.current_room is NULL:
                    errored_user.assigned_port.close()
                    self.active_user_list.remove(errored_user)
                    self.connection_list.remove(s)
                    self.num_active_users -= 1

                #if port logged in
                else:
                    remove_from = errored_user.current_room
                    remove_from.remove(errored_user)

                    errored_user.assigned_port.close()
                    self.active_user_list.remove(errored_user)
                    self.connection_list.remove(s)

                    self.num_active_users -= 1

    def login(self, user_name, passkey):
        """ Login function returns 1 if Username/Password match otherwise 0 """
        try:
            #poll database for user info
            userinfo = server_database.query_name(user_name)
            if userinfo[1] == passkey:
                return True
            else:
                sys.stderr.write("Incorrect password querry\n")
                return False
        except:
            #query_name couldn't find username, error message already in that function
            #try / except is here to avoid crashing when username is incorrect
            return False

    def register(self, in_user, user_name, passkey):
        """ Register function returns true if successfully registered otherwise false """
                
        banned_names = ('admin', 'administrator', 'server', 'SERVER', ' ', '0', 0, '', '\n', '\r', '\\')

        if user_name in banned_names:
            self.send_server_feedback(in_user, 'Cannot create an account with that name.\n')
            return False

        #store desired username and password in temp user, default alias to username
        to_register = database.stored_user(user_name, passkey, user_name) 

        #if successfully registered
        if server_database.insert(to_register) is True:
            sys.stderr.write ("Successfully registered with username: " + user_name
                + " to set an alias type /set_alias")
            self.send_server_feedback(in_user, 'successfully registered as new user!\n')
            in_user.username = user_name
            in_user.alias = user_name
            in_user.current_room = self.default_room
            self.default_room.users.append(in_user)
            return True
        
        else:
            self.send_server_feedback(in_user, 'Failed to register with that username. Username already taken.\n')
            return False
        
    def broadcast(self, in_message, in_room_name):
        """ Broadcast function for bradcasting a message to a chatroom. Takes a message class and a room name string. Returns true if succeeds, false if room is not found."""
        
        #lookup chatroom
        room_found = False
        for room in self.active_chatroom_list:
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
                    self.send_msg(user, in_message)
                
        #record to chat log

        return True

    def recv_msg(self, sock, msglen):
        """ Function to recieve a message from a socket as seperate parts. Returns a message class """                
        
        #Read raw data from socket
        data = sock.recv(msglen)

        #Find message metadata
        for active_u in self.active_user_list:

            #If regular message, bind user and room
            if active_u.assigned_port is sock:
                user = active_u
                chatroom = active_u.current_room
                break

            #If from not logged in user, keep empty username and room
            else:
                user = []
                chatroom = 0
        
        timestamp = str(datetime.now())
        text = str(data)
        
        #Build message class with data
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
        
        #find room and remove it
        for room in self.active_chatroom_list:
            if room.name is in_name:

                #empty users into default room
                for user in room.users:
                    user.current_room = self.default_room
                    self.default_room.users.append(user)
                    room.users.remove(user)
                
                #destroy room
                self.active_chatroom_list.remove(room)
                self.num_active_chatrooms -= 1
                sys.stderr.write('Successfully destroyed chat room named ' + in_name + '.\n')
                return True


        #room not found
        sys.stderr.write('Failed to destroy chatroom named ' + in_name + ' as it was not found.\n')
        return false