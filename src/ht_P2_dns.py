import socket
import time

DNS_IP = "127.0.0.1"
DNS_PORT = 5000

PRIMARY_IP = "127.0.0.1"
PRIMARY_PORT = 5001

BACKUP_IP = "127.0.0.1"
BACKUP_PORT = 5002

CURRENT_TARGET = (PRIMARY_IP, PRIMARY_PORT)

TIMEOUT = 3
last_primary_hb = time.time()
primary_alive = True
routing_state = "ROUTING_TO_PRIMARY"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((DNS_IP, DNS_PORT))
sock.settimeout(1)

print(f"DNS running... state = {routing_state}")

while True:
    current_time = time.time()

    if primary_alive and current_time - last_primary_hb > TIMEOUT:
        print("PRIMARY TIMEOUT DETECTED (DNS)")
        primary_alive = False
        CURRENT_TARGET = (BACKUP_IP, BACKUP_PORT)
        routing_state = "ROUTING_TO_BACKUP"
        print("PROMOTING BACKUP")
        print(f"DNS state = {routing_state}")

    try:
        data, addr = sock.recvfrom(1024)
        msg = data.decode()

        print(f"RECV from {addr}: {msg}")

        if msg.startswith("HB|PRIMARY|"):
            last_primary_hb = time.time()

            if not primary_alive:
                print("PRIMARY heartbeat resumed")

            primary_alive = True

            print(f"PRIMARY heartbeat received at {last_primary_hb}")

        elif msg.startswith("REQ|"):
            text = msg.split("|", 1)[1]

            forward_msg = f"REQ|{addr[0]}|{addr[1]}|{text}"
            sock.sendto(forward_msg.encode(), CURRENT_TARGET)

            print(f"FORWARD to ACTIVE SERVER: {forward_msg}")

        elif msg.startswith("RESP|"):
            _, client_ip, client_port, text = msg.split("|", 3)

            sock.sendto(text.encode(), (client_ip, int(client_port)))

            print(f"RETURN to CLIENT: {text}")

    except socket.timeout:
        pass