import datetime

class message(object):
    """This class is designed as a container for a clientside message and all details needed for simple handling"""
    

    
    def __init__(self, in_string):
        self.text = in_string

    def __init__(self, username, message_string):
        self.user = username
        self.content = message_string
        self.timestamp = datetime.now()
