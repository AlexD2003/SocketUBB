import socket
import threading

def send_message(sock):
    message = "Client message!"
    sock.send(message.encode())  # Send the message
    print("Message sent")

def receive_message(sock):
    buffer = sock.recv(1024)  # Receive message
    if buffer:
        print(f"Server reply: {buffer.decode()}")

def main():
    server_ip = "127.0.0.1"
    protocol = socket.SOCK_STREAM  # Default to TCP (SOCK_STREAM)
    
    # Adjust protocol if UDP is specified
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "UDP":
        protocol = socket.SOCK_DGRAM
    
    if len(sys.argv) > 2:
        server_ip = sys.argv[2]

    # Create socket
    sock = socket.socket(socket.AF_INET, protocol)
    
    # Setup server address
    server_address = (server_ip, 65432)
    
    # For TCP (SOCK_STREAM), connect to the server
    if protocol == socket.SOCK_STREAM:
        try:
            sock.connect(server_address)
        except socket.error as e:
            print(f"Connection failed: {e}")
            return
    
    # Start threads to send and receive messages
    send_thread = threading.Thread(target=send_message, args=(sock,))
    receive_thread = threading.Thread(target=receive_message, args=(sock,))
    
    send_thread.start()
    receive_thread.start()
    
    # Wait for both threads to finish
    send_thread.join()
    receive_thread.join()

    sock.close()  # Close the socket after communication is done

if __name__ == "__main__":
    main()
