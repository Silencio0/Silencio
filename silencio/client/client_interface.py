from client.client_network import network
import sys
import select
class interface(object):
    """Container for the basic text interface and its functions. Basically, just reads the messages to the command line"""
 
    def __init__(self):
        my_net = False
        

    def user_connect(self):
        """Prompts user for connection address and port, then attempts network connection."""
        while True:
            entered_address =  input('Enter server address:\n ')
            entered_port = input('Enter server port:\n ')
            self.my_net = network(entered_address, entered_port)
            if mynet is not False:
                print("Successfully connected.\n")
                return True

            else:
                print("Unable to connect to specified address, please try again.\n")
                
    def user_login(self):
        """Prompts user for username and password"""
        while True:
            entered_username =  input('Enter username or /register: ')
            if entered_username == "/register":
                entered_username = input('Enter desired username: ')
                entered_password = input ('Enter desired password: ')
                if network.register(entered_username, entered_password) == True:
                    print("Successfully registered with username: " + entered_username + "\n")
                    return True
                else:
                    print("Unsuccessful registration - try another username\n")
            else:
                entered_password = input('Enter password: ')
                if network.login(entered_username, entered_password) == True:
                    print("Successful login\n")
                    return True

                else:
                    print("Incorrect username/password, please try again.\n")
                    
    def user_listen(self):

        second_chance = False
        third_chance = False
        

    
        #listens for user input and sends message if there's input
        while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            user_input = sys.stdin.readline()
            if user_input:
                my_net.send_message(user_input)
        else:
            #listens for readable message and prints if available
            x = mynet.listen()
            if x != True and x != False and x != []:
                second_chance = False
                third_chance = False
                print_message(x)

            #if listen fails too much, then we return false on this.
            if x is False:
                second_chance = True
            if x is False and second_chance:
                third_chance = True
            if x is false and third_chance:
                my_net.disconnect()
                return False

    def print_message(self, message):
    	if message:
    		print(message)
    	


