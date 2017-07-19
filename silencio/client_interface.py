from .client_network import network

class interface(object):
    """Container for the basic text interface and its functions. Basically, just reads the messages to the command line"""
    

    def print_message(self, message):
    	if message:
    		print(message.content)
    	


