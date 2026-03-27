import socket
import threading

messages = []


def handle_client(client_socket, client_address):
    print(f"Пользователь с адресом: {client_address} подключился к серверу")

    with client_socket:
        data = client_socket.recv(1024)
        if data:
            message = data.decode()
            print(f"Пользователь с адресом: {client_address} отправил сообщение: {message}")
            messages.append(message)
            client_socket.send('\n'.join(messages).encode())


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('localhost', 12345))
        server_socket.listen(10)
        print("TCP сервер запущен на localhost:12345")

        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True,
            )
            thread.start()


if __name__ == "__main__":
    main()
