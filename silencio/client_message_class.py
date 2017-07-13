import datetime

class client_message(object):
    """This class is designed as a container for a clientside message and all details needed for simple handling"""
    
    is_incoming
    user
    content
    timestamp
    
    def __init__(self, username, message_string, time_sent):
        user = username
        content = message_string
        timestamp = time_sent

    def __init__(self, username, message_string):
        user = username
        content = message_string
        timestamp = datetime.time
