import datetime
from .server_active_user import active_user
from .server_active_chatroom import active_chatroom

class message(object):
    """The basic message class for moving messages in the server"""

    id
    sender
    room
    t_sent
    data
    message_type
