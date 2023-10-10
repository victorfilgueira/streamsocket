import socket
import sys
import threading

# Server configuration
SERVER_IP = '127.0.0.1'  # Can be the server's public IP
SERVER_PORT = 12345      # Choose an available port

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port and IP
server_socket.bind((SERVER_IP, SERVER_PORT))

# Start listening for connections
server_socket.listen(5)

print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

# Table of client information
client_table = {}

# Function to handle client connections
def handle_client(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break  # Client disconnected
        parts = message.split()
        command = parts[0]

        if command == "REGISTER":
            name, ip, port = parts[1], parts[2], parts[3]
            if name not in client_table:
                client_table[name] = (ip, port)
                client_socket.send("REGISTER_OK".encode())
                print(client_table)
            else:
                client_socket.send("REGISTER_EXISTING".encode())

        elif command == "SEARCH":
            name = parts[1]
            if name in client_table:
                ip, port = client_table[name]
                response = f"SEARCH_OK {name} {ip} {port}"
                client_socket.send(response.encode())
            else:
                client_socket.send("SEARCH_NONEXISTENT".encode())

        elif command == "DISCONNECT":
            client_socket.close()  # Fecha o socket do cliente
            print(f"Conexão encerrada com {client_socket.getpeername()}")
            break

# Função para lidar com a entrada do teclado e encerrar o servidor
def quit_server():
    while True:
        option = input("Pressione 'q' e Enter para encerrar o servidor: ")
        if option.lower() == 'q':
            print("Encerrando o servidor...")
            server_socket.close()  # Fecha o socket do servidor
            sys.exit()  # Encerra o programa
            
input_thread = threading.Thread(target=quit_server)
input_thread.daemon = True
input_thread.start()

# Accept connections and handle clients
while True:
    client_socket, address = server_socket.accept()
    print(f"Conexão estabelecida com {address[0]}:{address[1]}")
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()

# Remember to add error handling and gracefully terminate the server as needed.
# server_socket.close()
