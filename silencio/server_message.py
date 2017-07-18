import datetime
from .server_active_user import active_user
from .server_active_chatroom import active_chatroom

class message(object):
    """The basic message class for moving messages in the server"""

    def __init__ (self, user, chatroom, content, time):
        """ Default constructor for a message. """
        self.sender = user
        self.sent_in = chatroom
        self.timestamp = time
        self.string = content
        


    def parse_message_type(self):
        """ This is the bit that decides what kind of message it is. Returns a state for handling that type of message """
        #searches content for keywords, if found returns the keyword ex: /join 
        file = open(commands.txt, "r")
        for key_word in file:
        	if key_word in content:
        		return key_word
        	
        return "message"

