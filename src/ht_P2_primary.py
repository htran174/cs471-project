import socket

PRIMARY_IP = "127.0.0.1"
PRIMARY_PORT = 5001

DNS_IP = "127.0.0.1"
DNS_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((PRIMARY_IP, PRIMARY_PORT))

print("Primary running...")

while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode()

    print(f"RECV from {addr}: {msg}")

    if msg.startswith("REQ|"):
        _, client_ip, client_port, text = msg.split("|", 3)

        response = text.upper()

        send_msg = f"RESP|{client_ip}|{client_port}|{response}"
        sock.sendto(send_msg.encode(), (DNS_IP, DNS_PORT))

        print(f"SENT to DNS: {send_msg}")