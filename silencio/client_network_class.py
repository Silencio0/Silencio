class client_network(object):
    """This class is designed to handle network message sending and recieving for the client end"""
    import socket
    import datetime
    from .client_message_class import client_message
    from .client_message_table_class import client_message_table