# This file contains the information about the server address and the port and all other constants related to the chat.
import socket

SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5050
HEADER = 64
FORMAT = 'utf-8'
GROUP_SIZE = 5
DISCONNECT_MESSAGE = "disconnect"
NEWLINE_MESSAGE = "NEW_LINE"
EXCHANGE_MESSAGE = "EXCHANGE_MESSAGE"
NUMBER_BITS = 1024

MODE_MESSAGE = '''
*    Welcome to Cipher Sphere!                  *
*    Where your Texts are safe and encrypted    *
*    Enter the mode you want to use:            *
*    1. Establish Connection                    *
*    2. Connect                                 *
*    3. Exit                                    *
'''

EXIT_MESSAGE = '''
*    Thank you for using Cipher Sphere!         *
*    Have a nice day!                           *
'''

