import socket
import time
import os
import threading

HEADER = 64
PORT = 9955
SERVER = "127.0.0.1"
#SERVER = socket.gethostbyname(socket.gethostname())

FORMAT = 'utf-8'
DISCONNECT_msg = "Disconnect"
# print(SERVER)

# Creating socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specific server address and port
serverSocket.bind(("", PORT))


# Lock screen function
def lockScreen():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    pass


# A function to check if the student ID is valid
def isValid(studentID):
    validStudentIDs = {"1211088", "1200710", "1220062"}
    return studentID in validStudentIDs


# Function to handle communication with the client
# Function to handle communication with the client
def handleClient(conn, addr):
    print(f"[New Connection]{addr} connected")
    connected = True

    while connected:
        try:
            message_length = int(conn.recv(HEADER).decode(FORMAT))
        except ValueError:
            print(f"[{addr}] Error: Invalid message length.")
            continue

        message = conn.recv(message_length).decode(FORMAT)

        # Check if the message is a valid ID
        if isValid(message):
            # Display the message in the server's side
            print(f"[{addr}] Valid student ID received: {message} OS will lock screen after 10 seconds")

            # Send the message to the client
            conn.send(b"Server received a valid student ID. OS will lock screen after 10 seconds")

            # Wait for 10 seconds
            time.sleep(10)

            # Lock the screen
            lockScreen()

        elif message == DISCONNECT_msg:
            connected = False

        else:
            print(f"[{addr}] Invalid message received: {message}")
            # Tell the client that it is an invalid message
            conn.send(b"Error: Invalid message.")

    conn.close()

# Function to start the server
def start():
    # Listening for incoming connections
    serverSocket.listen(1)
    print(f"Server is listening on {SERVER}")
    while True:
        conn, addr = serverSocket.accept()
        # Create a new thread for each connected client
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    print("Server is starting..")
    start()