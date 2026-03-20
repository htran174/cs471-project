import socket
import time

PRIMARY_IP = "127.0.0.1"
PRIMARY_PORT = 5001

DNS_IP = "127.0.0.1"
DNS_PORT = 5000

BACKUP_IP = "127.0.0.1"
BACKUP_PORT = 5002

HEARTBEAT_INTERVAL = 1.0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((PRIMARY_IP, PRIMARY_PORT))
sock.settimeout(1)

last_heartbeat_time = 0

print("Primary running... state = ACTIVE")

while True:
    current_time = time.time()

    if current_time - last_heartbeat_time >= HEARTBEAT_INTERVAL:
        hb_msg = "HB|PRIMARY|ACTIVE"

        sock.sendto(hb_msg.encode(), (DNS_IP, DNS_PORT))
        print(f"SENT heartbeat to DNS: {hb_msg}")

        sock.sendto(hb_msg.encode(), (BACKUP_IP, BACKUP_PORT))
        print(f"SENT heartbeat to BACKUP: {hb_msg}")

        last_heartbeat_time = current_time

    try:
        data, addr = sock.recvfrom(1024)
        msg = data.decode()

        print(f"RECV from {addr}: {msg}")

        if msg.startswith("REQ|"):
            _, client_ip, client_port, text = msg.split("|", 3)

            response = text.upper()

            send_msg = f"RESP|{client_ip}|{client_port}|{response}"
            sock.sendto(send_msg.encode(), (DNS_IP, DNS_PORT))

            print(f"SENT to DNS: {send_msg}")

    except socket.timeout:
        pass