import socket

HOST = 'localhost'
PORT = 42424

def send_message(socket: socket, message: str):
    socket.send(bytes(message, "utf-8"))


def recive_message(socket: socket) -> str:
    data: bytes = socket.recv(1024)
    message = data.decode("utf-8")
    print(f"Server message {message}")
    if message.lower() == "quit":
        raise Exception()
    else:
        return message


def Main():
    s = socket.socket()
    s.connect((HOST, PORT))
    try:
        while True:
            send_message(s, "hej med dig")
            recive_message(s)
    except:
        s.close()


if __name__ == '__main__':
    Main()
