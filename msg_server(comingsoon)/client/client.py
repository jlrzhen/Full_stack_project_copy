from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time


class Client:
    """
    communication with server
    """

    HOST ="192.168.0.21" #private ip address, router's address that computers connected to the network will use to send data 
    PORT = 5500
    ADDR = (HOST,PORT)
    BUFSIZ = 512


    # constructor class
    def __init__(self,name):

        self.client_socket = socket(AF_INET,SOCK_STREAM) #a socket connecting to the network is created at each end of communication, this socket has a specific address
        self.client_socket.connect(self.ADDR)
        self.messages = []
        recieve_thread = Thread(target=self.recieve_messages)
        recieve_thread.start()
        self.send_message(name)
        self.lock = Lock()


    def recieve_messages(self):
        """
        recieve messages from server
        """

        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()

                # make sure message data is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()

            except Exception as e:
                print("[EXCEPTION]",e)
                break
    
    def send_messages(self,msg):
        """
        going to send messages to the server
        the type of value sent should be a string
        """

        try:
            self.client.socket.send(bytes(msg,"utf8"))
            if msg == "{quit}":
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET,SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)
    
    def get_messages(self):
        """
        :returns a list of str messages
        :return: list[str]
        """
        messages_copy = self.messages[:]

        # make sure memory is safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy
    
    def disconnect(self):
        self.send_message("{quit}")