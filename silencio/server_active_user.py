from .server_database import database

class active_user(object):
    """Class for handling active users logged into the server. Contains all info needed during active use."""

    username
    assigned_port
    client_addr
    current_room
    alias
    user_data
    blocked_users

    def __init__(self, sock, addr):
        """ Default active user constructor for users not signed in. Only holds the connection data, but not the user data. """
        username = NULL
        assigned_port = sock        
        client_addr = addr
        current_room = 0


    def __init__(self, user, sock, addr):
        """ connection constructor given the connecting address and the assigned socket. """
        username = user
        assigned_port = sock        
        client_addr = addr
        current_room = 0
        self.check_alias()

    def get_port():
        """Gives you the port assigned to the connection"""
        return assigned_port

    def get_addr():
        """Gives you the client address the connection"""
        return client_addr
    
    def get_current_room():
        """returns the current chatroom for the active user"""
        return current_room

    def check_alias():
        """Calls the database and confirms and sets the alias for a user"""
        alias = database.get_alias(username)

    def set_port(input_port):
        """Sets the current active port of the user to a user defined value"""
        assigned_port = input_port

    def set_current_room(input_room):
        """sets the current chat room of the active user to the inputted value, 0 is the default for not in a room."""
        current_room = input_room

    def log_in(in_user, in_pass):
        """Funtion to log in an active user. Checks login credentials against stored values. Sets the user data if correct, returns false if not"""
        login_info = database.get_password(in_user)

        #if username not in database
        if login_info is False:
            return False
        
        #if password matches username
        if in_pass is login_info:
            username = in_user
            current_room = 'default'
            self.check_alias()
            return True
        
        #if incorrect password
        else: 
            return False 

    def register(in_user, in_pass):
        """ Function that sets up new user info in the user database. Also logs in user. """
        #add user to database and login