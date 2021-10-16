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


def start_server():
    s = socket.socket()
    s.bind((HOST, PORT))

    s.listen(1)
    c, addr = s.accept()
    try:
        while True:
            send_message(c, recive_message(c).upper())
    except:
        c.close()


if __name__ == "__main__":
    start_server()
