class stored_user(object):

    #user that is saved into the database.  attributes are name, password, and alias. ID is assigned by database
    
    def __init__(self, name, password, alias):
        self.name = name
        self.password = password
        self.alias = alias


