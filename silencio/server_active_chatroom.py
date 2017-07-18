from .server_active_user import active_user

class active_chatroom(object):
    """Class for containing all active users in an active chat room."""

    def __init__ (self, in_name, in_owner):
        """ Default constructor for an active chatroom. Requires a name. """
        self.name = in_name
        self.users = []
        self.owner = in_owner

    def add_user (self, in_user):
        """ Function for adding a user to the chatroom. Returns true if succeeds, false if user is already in chatroom."""

        #check for user already in chatroom
        for u in self.users:
            if u is in_user:
                return false

        #if not, add to list
        in_user.current_room = self.name
        self.users.append(in_user)
        return true

    def remove_user (self, in_user):
        """ Function for removing a user from a chatroom. Returns false if user is not found, true if user is removed. """
    
        #check for user already in chatroom
        for u in self.users:
            if u is in_user:
                self.users.remove(u)
                return true
        
        #user not found
        return false
