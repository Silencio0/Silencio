from server.server_database import database

class active_user(object):
    """Class for handling active users logged into the server. Contains all info needed during active use."""
    

    def __init__(self, sock, addr):
        """ Default active user constructor for users not signed in. Only holds the connection data, but not the user data. """
        self.username = NULL
        self.assigned_port = sock        
        self.client_addr = addr
        self.current_room = []
        self.blocked_users = []

    def __init__(self, user, sock, addr):
        """ connection constructor given the connecting address and the assigned socket. """
        self.username = user
        self.assigned_port = sock        
        self.client_addr = addr
        self.current_room = []
        self.check_alias()
        self.blocked_users = []

    def get_port(self):
        """Gives you the port assigned to the connection"""
        return self.assigned_port

    def get_addr(self):
        """Gives you the client address the connection"""
        return self.client_addr
    
    def get_current_room(self):
        """returns the current chatroom for the active user"""
        return self.current_room

    def get_alias(self):
        
        return self.alias

    def check_alias(self):
        """Calls the database and confirms and sets the alias for a user"""
        self.alias = database.retrieve_alias(self)


    def set_port(self, input_port):
        """Sets the current active port of the user to a user defined value"""
        self.assigned_port = input_port

    def set_current_room(self, input_room):
        """sets the current chat room of the active user to the inputted value, 0 is the default for not in a room."""
        self.current_room = input_room

    def log_in(in_user, in_pass):
        """Funtion to log in an active user. Checks login credentials against stored values. Sets the user data if correct, returns false if not"""
        login_info = database.retrieve_password(in_user)

        #if username not in database
        if login_info is False:
            return False
        
        #if password matches username
        if in_pass is login_info:
            self.username = in_user
            self.current_room = 'default'
            self.check_alias()
            return True
        
        #if incorrect password
        else: 
            return False 
