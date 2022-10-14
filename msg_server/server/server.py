# Background Notes:

# going to make a simple chat room server that allows multiple clients to connect to it
# going to use Sockets - endpoints in a communication channel
# sockets are bidirectional and establish communication between a server and multiple clients
# multi-threading is a sub-process that runs a set of commands individually, everytime a user connects to the server a seperate thread is created for that user, will require two scripts to establish chat room one to keep server running and another that clients should run

# Server Side script
# establish a socket + bind it to ip address + port specified to a port number
# everytime a user connects seperate threads will be created for that user, in each thread server waits for a message and sends that message to other users currently on the chat

# if server is meant to be accessible beyond a local network, public IP address would be required for usage
# IMPORTANT - this requires PORT FORWARDING

# AF_INET is address domain of socket, used when we han an Internet Domain with any two hosts, SOCK_STREAM is type of socket, data or characters are read in a continuous flow 
# UTF-8 is an encoding system for Unicode. It can translate any Unicode character to a matching unique binary string

from socket import AF_INET,socket,SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR
from threading import Thread

import time
from student import Student

#Global constants
HOST = 'localhost'
PORT = 5500 #port number
BUFSIZ = 512 # buffer-size, max amount of bits of data server recieves
MAX_CONNECTIONS = 10 #the max amount of connections in a single chatroom
ADDR = (HOST,PORT) #the address is the name of the host, localhost, and the port number


#Global Variables
students = []
SERVER = socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR) #sets up the server at this address (right now its a port on the local machine/ personal computer)


def broadcast(msg, name):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return:
    """
    for student in students:
        client = student.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION]", e)

def accept_incoming_connections():
    # Wait for connection from new clients, start new thread once connected
    # param Server:SOCKET 
    # return: None

    # go into an infinite loop and wait for connections from many different clients
    # sometimes this fails so we want to have a try, except block as a failsafe 
    while True:
        try:
            #accept the 
            client,addr = SERVER.accept()
            student = Student(addr,client)
            students.append(student)

            print(f"[LINKED]{addr} has landed in the server at {time.time()}")
            Thread(target=client_communication,args=(client,)).start()
        # when any exception case comes up, causing the loop to fail/crash, we will output a message to the screen with the message, Failure and the type of error, 'e', it was
        except Exception as e:
            print("[Failure]",e)
            break
    print("[SERVER CRASHED] SESSION TERMINATED")

# create client object and each client object is going to store an address
def client_communication(student):
    """
    Thread to handle all messages from client
    :param client: socket
    :return: None

    """
    client = student.client

    # first message received is always the studentss name
    name = client.recv(BUFSIZ).decode("utf8")
    student.set_name(name)

    msg = bytes(f"Welcome fellow IB student! {name} has joined the chat!", "utf8")
    broadcast(msg, "")  # broadcast welcome message

    run = True
    while run: #wait for message from student
        msg = client.recv(BUFSIZ)
        # if we send a message that we have left the server, we will broadcast that the user has left the server
        if msg != bytes("{quit}","utf8"):
            client.close()
            students.remove(student)
            broadcast(bytes(f"{name} has left the chat...", "utf8"),"")

        else: #send message(s) to all other clients
            broadcast(msg,name+": ")
            print(f"{name}:", msg.decode("utf8"))    



if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) #listen for 10 connections
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target= accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()