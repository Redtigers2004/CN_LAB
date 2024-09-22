#include <stdio.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")  

int main()
{
    WSADATA wsa;
    SOCKET server_socket, client_socket;
    struct sockaddr_in server_addr, client_addr;
    int client_addr_len = sizeof(client_addr);
    char buffer[1024];
    WSAStartup(MAKEWORD(2, 2), &wsa);
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(5566);
    bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr));
    listen(server_socket, 3);
    printf("[+]TCP server socket created.\n[+]Bind to the port number: 5566\nListening...\n");
    client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_addr_len);
    memset(buffer, 0, sizeof(buffer));
    recv(client_socket, buffer, sizeof(buffer), 0);
    printf("Client: %s\n", buffer);
    send(client_socket, "Hello from server!", 18, 0);
    closesocket(client_socket);
    closesocket(server_socket);
    WSACleanup();
    
    return 0;
}


