import datetime

class message(object):
    """This class is designed as a container for a clientside message and all details needed for simple handling"""
    

    
    def __init__(self, username, message_string, time_sent):
        self.user = username
        self.content = message_string
        self.timestamp = time_sent

    def __init__(self, username, message_string):
        self.user = username
        self.content = message_string
        self.timestamp = datetime.now()
