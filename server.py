import socket
import sys
import threading

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    data = conn.recv(1024)
    if data:
        print(f"Received: {data.decode()}")
        conn.sendall(b"Server message!")
    conn.close()

def start_server(host, port, protocol):
    with socket.socket(socket.AF_INET, protocol) as s:
        s.bind((host, port))
        if protocol == socket.SOCK_STREAM:
            s.listen()
            print(f"Server listening on {host}:{port} (TCP)...")
            while True:
                conn, addr = s.accept()
                # Create a new thread for each client connection
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.start()
        else:  # UDP
            print(f"Server listening on {host}:{port} (UDP)...")
            while True:
                data, addr = s.recvfrom(1024)
                print(f"Received: {data.decode()} from {addr}")
                s.sendto(b"Server message!", addr)

HOST = '0.0.0.0'
PORT = 65432
protocol = socket.SOCK_STREAM  

if len(sys.argv) > 1 and sys.argv[1] == 'UDP':
    protocol = socket.SOCK_DGRAM
if len(sys.argv) > 2:
    HOST = sys.argv[2] 

start_server(HOST, PORT, protocol)
