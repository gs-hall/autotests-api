import socket


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    client_socket.send("Привет, сервер!".encode())
    client_socket.shutdown(socket.SHUT_WR)
    print(client_socket.recv(1024).decode())
    client_socket.close()


if __name__ == "__main__":
    main()
