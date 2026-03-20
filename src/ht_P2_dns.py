import socket

DNS_PORT = 5000
PRIMARY_IP = "127.0.0.1"
PRIMARY_PORT = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", DNS_PORT))

print("DNS running...")

while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode()

    print(f"RECV from {addr}: {msg}")

    # If message is from client
    if msg.startswith("REQ|"):
        text = msg.split("|")[1]

        forward_msg = f"REQ|{addr[0]}|{addr[1]}|{text}"
        sock.sendto(forward_msg.encode(), (PRIMARY_IP, PRIMARY_PORT))

        print(f"FORWARD to PRIMARY: {forward_msg}")

    # If message is from primary
    elif msg.startswith("RESP|"):
        _, client_ip, client_port, text = msg.split("|")

        sock.sendto(text.encode(), (client_ip, int(client_port)))

        print(f"RETURN to CLIENT: {text}")