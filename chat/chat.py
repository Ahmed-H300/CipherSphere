from config import *

# this module is for the chat module
class Chat:
    def __init__(self):
        print(MODE_MESSAGE)
        self.mode = input("Enter the mode: ")
        if self.mode == "1":
            self.establish_connection()
        elif self.mode == "2":
            self.connect()
        elif self.mode == "3":
            print(EXIT_MESSAGE)
            exit()
        ######################################
        self.server_address = SERVER_ADDRESS
        self.server_port = SERVER_PORT
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_address, self.server_port))
        self.username = input("Enter your username: ")
        self.client.send(self.username.encode(FORMAT))
        self.server_response = self.client.recv(HEADER_SIZE).decode(FORMAT)
        print(self.server_response)
        self.group = input("Enter the group name: ")
        self.client.send(self.group.encode(FORMAT))
        self.server_response = self.client.recv(HEADER_SIZE).decode(FORMAT)
        print(self.server_response)
        self.start_chat()

    def establish_connection(self):
        pass

    def connect(self):
        pass

    def start_chat(self):
        while True:
            self.message = input(f"{self.username} > ")
            self.client.send(self.message.encode(FORMAT))
            if self.message == "exit":
                break
            self.server_response = self.client.recv(HEADER_SIZE).decode(FORMAT)
            print(f"{self.group} > {self.server_response}")
        self.client.close()