from .server_stored_user import stored_user
from .server_stored_chatroom import stored_chatroom

import pymysql
#need pymysql because mysql does not have python 3 support

"""Database class for the server that is designed to cold store all user and chatroom info"""

class database(object):

    #this will change if we run off nolans computer. will update if/when necessary
    db = ("localhost", "Avery", "test", "CHAT_DATABASE")

    def __init__(self):
        self.con = pymysql.connect(*self.db)
        self.cursor = self.con.cursor()
     
#inserts a user if the user isn't already there.
    def insert(self, user):

        if self.query_name(user.name) is None:
            self.cursor.execute("""INSERT into users VALUES (NULL, %s, %s, %s)""",(user.name,
                user.password,user.alias))
            self.con.commit()
        else:
            print ("ID already taken")

#query finds a user given the id and returns the user if found
    def query_id(self, id):
        self.cursor.execute("""SELECT * from users WHERE id =(%s)""",(id))           
        temp = self.cursor.fetchone()

        #If a user is found, return it
        if temp is not None:
            temp_user = user(temp[1],temp[2], temp[3]) 
            return temp_user
        else:
            print ("No User Matching That ID")
 #query finds a user given the name and returns the user if found       
    def query_name(self, name):
        self.cursor.execute("""SELECT * from users WHERE name =(%s)""",(name))           
        temp = self.cursor.fetchone()

        #If a user is found, return it
        if temp is not None:
            temp_user = user(temp[1],temp[2], temp[3]) 
            return temp_user
        else:
            print ("No User Matching That Name") 

#retrieves an id of a given user 
    def retrieve_id(self, user):
        self.cursor.execute("""SELECT id from users WHERE name=(%s)""",(user.name))
        temp = self.cursor.fetchone()
        if temp is not None:
            return temp[0]
        else:
            print ("No id matching that id")

#sets an alias for a user    
    def set_alias(self, alias, user):
        self.cursor.execute("""UPDATE users SET alias = (%s) WHERE name = (%s)""", (alias, user.name))
        self.con.commit()
        user.alias = alias

#returns total number of users
    def num_users(self):
        self.cursor.execute("""SELECT COUNT(*) FROM users""")
        temp = self.cursor.fetchone()
        if temp is not None:
            return temp[0]
        else:
            print ("Table is empty")
