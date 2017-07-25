from .client_network import network
import sys
import select
class interface(object):
    """Container for the basic text interface and its functions. Basically, just reads the messages to the command line"""
    
    def user_login(self):
    	"""Prompts user for username and password"""
    	while True:
    		entered_username =  input('Enter username or /register: ')
    		if entered_username == "/register":
    			entered_username = input('Enter desired username: ')
    			entered_password = input ('Enter desired password: ')
    			if network.register(entered_username, entered_password) == True:
    				print("Successfully registered with username: " + entered_username + "\n")
    				return
    			else:
    				print("Unsuccessful registration - try another username\n")
	    	else:
	    		entered_password = input('Enter password: ')
	    		if network.login(entered_username, entered_password) == True:
	    			print("Successful login\n")
	    			return
	    		print("Incorrect username/password\n")
 
    def user_listen(self):
    	#listens for user input and sends message if there's input
    	while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
    		user_input = sys.stdin.readline()
    		if user_input:
    			network.send_message(user_input)
    	else:
    		#listens for readable message and prints if available
    		x = network.listen()
    		if x != True and x != False and x != []:
    			print_message(x)

    def print_message(self, message):
    	if message:
    		print(message)
    	


