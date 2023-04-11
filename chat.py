import socket
import sys
from inputimeout import inputimeout
import threading
import queue
from config import *
from security import *
from utils import *
DEBUG_activate = False

# this module is for the chat module
class Chat:
    def __init__(self):
        self.server_address = SERVER_ADDRESS
        self.server_port = SERVER_PORT
        self.writing = False
        self.q  = queue.Queue()
        self.rsa = RSA(NUMBER_BITS)
        self.mode = ''
        self.server = None
        self.conn = None
        self.addr = None
        self.threadrec  = None
        self.threadsen = None
        self.client = None
        print('public debug      :', str(self.rsa.public_key)) if DEBUG_activate else None
        print('private debug     :', str(self.rsa.private_key)) if DEBUG_activate else None
        self.menu()

    def menu(self):
        print(MODE_MESSAGE)
        self.mode = input("Enter the mode: ")
        if self.mode == "1":
            self.serverMode()
        elif self.mode == "2":
            self.clientMode()
        elif self.mode == "3":
            print(EXIT_MESSAGE)
            exit()
        else:
            print('WRONG INPUT')
            exit()


    def serverMode(self):
        ADDR = (self.server_address, self.server_port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        print('Server is established...')
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.server_address}:{self.server_port}")
        print('Waiting for the other side to connect...')
        self.conn, self.addr = self.server.accept()
        print("[ACTIVE CONNECTION] [Connection is activated]")
        stop_event = threading.Event()
        self.exchangeKeys(self.conn)
        print('Keys are exchanged...')
        print('Start Chatting. Have Fun :)')
        self.threadrec = threading.Thread(target=self.recieve_mess, args=(stop_event,))
        self.threadsen = threading.Thread(target=self.send_mess, args=(stop_event,))
        self.threadrec.start()
        self.threadsen.start()
        while not stop_event.is_set():
            while (not self.q.empty()) and (not self.writing):
                msg = self.q.get()
                if msg == DISCONNECT_MESSAGE:
                    stop_event.set()
                else:
                    print(msg)

        print("[INACTIVE CONNECTION] [Connection is deactivated]")
        self.threadrec.join()
        self.threadsen.join()

        self.conn.close()
        self.server.close()

        print('Connections are closed')

        self.menu()
        
    def recieve_mess(self, stop_event):
        conn = None
        addr = None
        if self.mode == '1':
            conn = self.conn
            addr = self.addr
        else:
            conn = self.client
            addr = self.addr
        while not stop_event.is_set():
            nl = False
            ex = False
            message = ''
            conn.settimeout(1)
            while (not nl) and (not stop_event.is_set()):
                try:
                    msg_length = conn.recv(HEADER).decode(FORMAT)
                    if msg_length:
                        conn.settimeout(None)
                        msg_length = int(msg_length)
                        msg = conn.recv(msg_length).decode(FORMAT)
                        if msg == NEWLINE_MESSAGE:
                            nl = True
                        elif msg == EXCHANGE_MESSAGE:
                            ex = True
                        else:
                            if ex:
                                message += (msg)
                            else:
                                msg =int(msg)
                                msg = self.rsa.decrypt_word(msg)
                                message += decode_word(msg)
                except:
                    continue
            if message != '':
                self.q.put(f"[{addr}] {message}")
            if message == DISCONNECT_MESSAGE:
                self.q.put(f"{message}")
                

    def recieve_text(self, conn):
        nl = False
        ex = False
        message = ''
        while not nl:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == NEWLINE_MESSAGE:
                    nl = True
                elif msg == EXCHANGE_MESSAGE:
                    ex = True
                else:
                    if ex:
                        message += (msg)
                    else:
                        msg =int(msg)
                        msg = self.rsa.decrypt_word(msg)
                        message += decode_word(msg)
        return message

    def send_mess(self, stop_event):
        conn = None
        if self.mode == '1':
            conn = self.conn
        else:
            conn = self.client
        while not stop_event.is_set():
            try:
                message = inputimeout(timeout=1)
                if message == '':
                    self.writing = True
                    print('>>', end=' ')
                    message = input()
                    self.send_text(message, conn)
                    self.writing = False
                    if message == DISCONNECT_MESSAGE:
                        self.q.put(f"{message}")
            except:
                sys.stdout.write('\033[F')  # move the cursor up one line
                sys.stdout.write('\033[K')  # clear the current line
                sys.stdout.write('\r')  # move the cursor to the beginning of the line
                sys.stdout.flush()  # make sure the output is flushed to the console
                continue

    def send_text(self, mess, conn):
        message = mess
        if isinstance(message, tuple):
            message = str(message)
            message = [EXCHANGE_MESSAGE, message]
        else: 
            message = self.rsa.encrypt_text(encode_text(message))
            message = [str(num) for num in message]
        message.append(NEWLINE_MESSAGE)
        for m in message:
            m = m.encode(FORMAT)
            message_length = len(m)
            send_length = str(message_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            conn.send(send_length)
            conn.send(m)

    def clientMode(self):
        client_address = input('Enter address to connect to: ')
        client_port = input('Enter port to connect to: ')
        ADDR = (client_address, int(client_port))
        self.addr = str(ADDR)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        print('Client is connected...')
        stop_event = threading.Event()
        self.exchangeKeys(self.client)
        print('Keys are exchanged...')
        print('Start Chatting. Have Fun :)')
        # self.connected = True
        self.threadrec = threading.Thread(target=self.recieve_mess, args=(stop_event,))
        self.threadsen = threading.Thread(target=self.send_mess, args=(stop_event,))
        self.threadrec.start()
        self.threadsen.start()
        while not stop_event.is_set():
            while (not self.q.empty()) and (not self.writing):
                msg = self.q.get()
                if msg == DISCONNECT_MESSAGE:
                    stop_event.set()
                else:
                    print(msg)

        print("[INACTIVE CONNECTION] [Connection is deactivated]")
        self.threadrec.join()
        self.threadsen.join()


        self.client.close()

        print('Connections are closed')

        self.menu()


    def exchangeKeys(self, conn):
        if self.mode == '1':
            self.send_text(self.rsa.public_key, conn)
            self.rsa.set_other_public_key(self.recieve_text(conn))
        else:
            self.rsa.set_other_public_key(self.recieve_text(conn))
            self.send_text(self.rsa.public_key, conn)

        print('DEBUG     :',self.rsa.e_other, self.rsa.n_other) if DEBUG_activate else None



if __name__ == "__main__":
    chat = Chat()
