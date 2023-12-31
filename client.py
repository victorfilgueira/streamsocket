import socket

# Server config
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345    

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to server
client_socket.connect((SERVER_IP, SERVER_PORT))

# Função para registrar o cliente no servidor
def register_client(name, ip, port):
    message = f"REGISTER {name} {ip} {port}"
    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    return response

# Função para consultar um cliente por nome
def search_client(name):
    message = f"SEARCH {name}"
    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    return response

# Função para solicitar desconexão
def disconnect():
    message = "DISCONNECT"
    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    return response

while True:
    print("\nMenu:")
    print("1. Registrar-se")
    print("2. Consultar")
    print("3. Desconectar")
    print("4. Sair")

    choice = input("Escolha uma opção: ")

    if choice == "1":
        name = input("Insira o nome do cliente: ")
        ip = input("Insira o IP do cliente: ")
        port = input("Insira a porta do cliente: ")
        result = register_client(name, ip, port)
        print(result)
    
    elif choice == "2":
        name = input("Insira o nome do cliente para consulta: ")
        result = search_client(name)
        print(result)
    
    elif choice == "3":
        result = disconnect()
        print(result)
    
    elif choice == "4":
        break

    else:
        print("Escolha inválida. Por favor selecione uma opção válida.")