from server.server_stored_user import stored_user

import pymysql
#need pymysql because mysql does not have python 3 support

"""Database class for the server that is designed to cold store all user and chatroom info"""

class database(object):

    #this will change if we run off nolans computer. will update if/when necessary
  
    def __init__(self):
        self.con = pymysql.connect(host = "96.54.58.48", port = 3306, user = "remoteUser",passwd =  "test", db = "CHAT_DATABASE")
        self.cursor = self.con.cursor()
     
#inserts a user if the user isn't already there.
    def insert(self, user):

        if self.query_name(user.name) is None:
            self.cursor.execute("""INSERT into users VALUES (NULL, %s, %s, %s, NULL)""",(user.name,
                user.password,user.alias))
            self.con.commit()
            return True
        else:
            print ("ID already taken")
            return False

#query finds a user given the id and returns the user if found
    def query_id(self, id):
        self.cursor.execute("""SELECT * from users WHERE id =(%s)""",(id))           
        temp = self.cursor.fetchone()

        #If a user is found, return it
        if temp is not None:
            temp_user = stored_user(temp[1],temp[2], temp[3]) 
            return temp_user
        else:
            print ("No User Matching That ID")

#query finds a user given the name and returns the user if found       
    def query_name(self, name):
        self.cursor.execute("""SELECT * from users WHERE name =(%s)""",(name))           
        temp = self.cursor.fetchone()
        
        #If a user is found, return it
        if temp is not None:
            temp_user = stored_user(temp[1],temp[2], temp[3]) 
            return temp_user
        else:
            print ("No User Matching That Name") 
            return False

#retrieves an id of a given user 
    def retrieve_id(self, user):
        self.cursor.execute("""SELECT id from users WHERE name=(%s)""",(user.name))
        temp = self.cursor.fetchone()
        if temp is not None:
            return temp[0]
        else:
            print ("No id matching that id")

#Returns a password of a certain user.
    def retrieve_password(self, user):
        self.cursor.execute("""SELECT password from users WHERE name=(%s)""",(user.name))
        temp = self.cursor.fetchone()
        if temp is not None:
            return temp[0]
        else:
            return None
        
#Returns alias of a certain user.
    def retrieve_alias(self, username):
        self.cursor.execute("""SELECT alias from users WHERE name=(%s)""",(username))
        temp = self.cursor.fetchone()
        if temp is not None:
            return temp[0]
        else:
            return None
        
#Returns all of the blocked users (in a string of IDs) of a certain user.
    def retrieve_blocked_users(self, user):
        self.cursor.execute("""SELECT blocked_users from users WHERE name=(%s)""",(user.name))
        temp = self.cursor.fetchone()
        if temp is not None:
            return temp[0]
        else:
            return None
        
#sets an alias for a user    
    def set_alias(self, alias, user):
        self.cursor.execute("""UPDATE users SET alias = (%s) WHERE name = (%s)""", (alias, user.name))
        self.con.commit()
        user.alias = alias

#blocks a user(blocked) for another user(blocker)
    def block_user(self, blocker, blocked):
    
        if blocker.name is blocked.name:
            print("Can't block yourself")
            return False
        list_blocked = self.retrieve_blocked_users(blocker)
        blocked_id =  str(self.retrieve_id(blocked))
        
        if  list_blocked is  None:                #if no one is blocked yet, start new list
            list_blocked = []
        else:
            list_blocked = list_blocked.split(",")

        if blocked_id in list_blocked:            #checks to see if user is already blocked
            print("User is Already Blocked")
            return False
        else:
            list_blocked.append(blocked_id)       #adds user to list of blocked users
            list_blocked = ",".join(list_blocked)
            if list_blocked[0] == ',': del list_blocked[0]
            self.cursor.execute("""UPDATE users SET blocked_users = (%s) WHERE name = (%s)""", (list_blocked, blocker.name))
            self.con.commit()                     #commits block
            return True


#unblocks a user(blocked) for another user(blocker)
    def unblock_user(self, blocker, blocked):
    
        list_blocked = self.retrieve_blocked_users(blocker)
        blocked_id =  str(self.retrieve_id(blocked))

        if  list_blocked is not None:             #checks to see if any users are blocked
            list_blocked = list_blocked.split(",")
            if blocked_id in list_blocked:        #checks to see if specific user is blocked
                list_blocked.remove(blocked_id)
                if list_blocked:                  #if there are still blocked users, add them back to the db
                    list_blocked = ",".join(list_blocked)
                    if list_blocked[0] == ',': del list_blocked[0]
                else:
                    list_blocked = None    
                self.cursor.execute("""UPDATE users SET blocked_users = (%s) WHERE name = (%s)""", (list_blocked, blocker.name))
                self.con.commit()                 #commit changes to the db
                return True
            else: 
                print("User is not blocked")
                return False
        else: 
            print("No users blocked")
            return False

#Returns True or False is a user is blocked by another user.
    def is_blocked(self, blocker, blocked):

        list_blocked = self.retrieve_blocked_users(blocker)
        blocked_id =  str(self.retrieve_id(blocked))
        if  list_blocked is not None:
            list_blocked = list_blocked.split(",")
            if blocked_id in list_blocked: return True
        else:
            return False

#returns total number of users
    def num_users(self):
        self.cursor.execute("""SELECT COUNT(*) FROM users""")
        temp = self.cursor.fetchone()
        if temp is not None:
            return temp[0]
        else:
            print ("Table is empty")
