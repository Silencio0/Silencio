import datetime
from .server_connection import connection
from .server_active_user import active_user
from .server_active_chatroom import active_chatroom
from .server_connection import connection

class network(object):
    """Server network class that does all the hard stuff."""
    num_connections
    connection_list
    num_active_users
    active_user_list
    num_active_chatrooms
    active_chatroom_list

