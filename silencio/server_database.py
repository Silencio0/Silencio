from .server_stored_user import stored_user
from .server_stored_chatroom import stored_chatroom


class database(object):
    """Database class for the server that is designed to cold store all user and chatroom info"""

    num_users
    num_rooms
    rooms
    users
