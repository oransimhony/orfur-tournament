import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    my_socket.sendto("Oran", ("127.0.0.1", 8888))

    (data, addr) = my_socket.recvfrom(1024)

    print "The server sent: " + data

my_socket.close()