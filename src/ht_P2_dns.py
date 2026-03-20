import socket

DNS_IP = "127.0.0.1"
DNS_PORT = 5000

PRIMARY_IP = "127.0.0.1"
PRIMARY_PORT = 5001

CURRENT_TARGET = (PRIMARY_IP, PRIMARY_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((DNS_IP, DNS_PORT))

print("DNS running...")

while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode()

    print(f"RECV from {addr}: {msg}")

    # Message from client
    if msg.startswith("REQ|"):
        text = msg.split("|", 1)[1]

        forward_msg = f"REQ|{addr[0]}|{addr[1]}|{text}"
        sock.sendto(forward_msg.encode(), CURRENT_TARGET)

        print(f"FORWARD to ACTIVE SERVER: {forward_msg}")

    # Message from server
    elif msg.startswith("RESP|"):
        _, client_ip, client_port, text = msg.split("|", 3)

        sock.sendto(text.encode(), (client_ip, int(client_port)))

        print(f"RETURN to CLIENT: {text}")