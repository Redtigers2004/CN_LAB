#include<stdio.h>
#include<winsock2.h>

#pragma comment (lib,"ws2_32.lib")

int main()
{
    WSADATA wsa;
    SOCKET sock;
    struct sockaddr_in server_addr;
    char buffer[1024];
    WSAStartup(MAKEWORD(2,2),&wsa);
    sock = socket(AF_INET,SOCK_STREAM,0);
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(5566);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    if(connect(sock,(struct sockaddr *)&server_addr,sizeof(server_addr))<0)
    {
        printf("connection failed\n");
        return 1;
    }
    send(sock,"Hello from Client!",18,0);
    memset(buffer,0,sizeof(buffer));
    recv(sock, buffer,sizeof(buffer),0);
    printf("Server: %s\n",buffer);
    closesocket(sock);
    WSACleanup();
    return 0;
}












