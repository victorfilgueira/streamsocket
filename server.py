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

print(f"...Servidor iniciado em {SERVER_IP}:{SERVER_PORT}\n")

# Table of client information
client_table = {}

server_running = True

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
            if name not in client_table and all(client[0] != ip for client in client_table.values()):
                client_table[name] = (ip, port)
                print(f'\nCLIENTE "{name}" REGISTRADO COM SUCESSO!\n')
                client_socket.send("\nREGISTRADO COM SUCESSO!\n".encode())
                print(client_table)
            else:
                client_socket.send("\nCLIENTE JÁ REGISTRADO!\n".encode())

        elif command == "SEARCH":
            name = parts[1]
            if name in client_table:
                ip, port = client_table[name]
                response = f"\nNome: {name}, IP: {ip}, Porta: {port}\n"
                client_socket.send(response.encode())
            else:
                client_socket.send("\nCLIENTE NÃO ENCONTRADO!".encode())

        elif command == "DISCONNECT":
            response = "Encerrando conexão...\n"
            client_socket.send(response.encode())
            client_socket.close()  # Fecha o socket do cliente
            print(f"Conexão encerrada com {client_socket.getpeername()}\n")
            server_running = False
            sys.exit()
            break

def quit_server():
    global server_running
    while True:
        option = input()
        if option.lower() == 'q':
            print("Encerrando o servidor...\n")
            server_running = False
            server_socket.close()  # Fecha o socket do servidor
            sys.exit()  # Encerra o programa
            
input_thread = threading.Thread(target=quit_server)
input_thread.daemon = True
input_thread.start()

# Accept connections and handle clients
while server_running:
    client_socket, address = server_socket.accept()
    print(f"Conexão estabelecida com {address[0]}:{address[1]}\n")
    if server_running:
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
        
# Aguardar a conclusão de todas as threads de clientes antes de encerrar o programa
for thread in threading.enumerate():
    if thread != threading.main_thread():
        thread.join()
