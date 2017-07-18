import datetime
from .server_active_user import active_user
from .server_active_chatroom import active_chatroom

class message(object):
    """The basic message class for moving messages in the server"""

    def __init__ (self, user, chatroom, content):
        """ Default constructor for a message. """
        sender = user
        sent_in = chatroom
        string = content


    def parse_message_type(self):
        """ This is the bit that decides what kind of message it is. Returns a state for handling that type of message """
