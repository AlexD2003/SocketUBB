#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <thread>

void send_message(int sock) {
    std::string message = "Client message!";
    send(sock, message.c_str(), message.size(), 0);
    std::cout << "Message sent\n";
}

void receive_message(int sock) {
    char buffer[1024] = {0};
    int valread = read(sock, buffer, 1024); 
    if (valread > 0) {
        std::cout << "Server reply: " << buffer << "\n";
    }
}

int main(int argc, char *argv[]) {
    int sock = 0;
    struct sockaddr_in serv_addr;

    std::string server_ip = "127.0.0.1";
    int protocol = SOCK_STREAM; 
    if (argc > 1 && std::string(argv[1]) == "UDP") {
        protocol = SOCK_DGRAM; 
    }
    if (argc > 2) {
        server_ip = argv[2]; 
    }

    sock = socket(AF_INET, protocol, 0);
    if (sock < 0) {
        std::cerr << "Socket creation error\n";
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(65432);

    if (inet_pton(AF_INET, server_ip.c_str(), &serv_addr.sin_addr) <= 0) {
        std::cerr << "Invalid address\n";
        return -1;
    }

    if (protocol == SOCK_STREAM) {
        if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
            std::cerr << "Connection failed\n";
            return -1;
        }
    }

    std::thread send_thread(send_message, sock);
    std::thread receive_thread(receive_message, sock);

    send_thread.join();
    receive_thread.join();

    close(sock);
    return 0;
}
