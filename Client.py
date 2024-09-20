import socket

HEADER = 64
PORT = 9955
#SERVER = "127.0.0.1"
SERVER = socket.gethostbyname(socket.gethostname())
# ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_msg = "Disconnect"

# Creating socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((SERVER,PORT))

def send(msg) :
    message = msg.encode(FORMAT)
    messageLength = len(message)
    sendLength = str(messageLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))
    clientSocket.send(sendLength + message)

# Allow the user to input the message
userMessage = input("Enter your message to the server: ")

# Send a message to the server
send(userMessage)

# Send a disconnect message
send(DISCONNECT_msg)
