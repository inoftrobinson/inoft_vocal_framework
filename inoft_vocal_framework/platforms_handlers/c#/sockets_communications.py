from socket import *

def start_socket():
    while True:
        print("hey")
        PySocket = socket(AF_INET, SOCK_DGRAM)
        PySocket.bind(('127.0.0.1', 9999))
        PySocket.send(b"Salut ! :)")
        data, client = PySocket.recvfrom(1024)
        print(data)


# todo: make the socket reading async
if __name__ == "__main__":
    start_socket()

