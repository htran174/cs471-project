import socket
import time

BACKUP_IP = "127.0.0.1"
BACKUP_PORT = 5002

DNS_IP = "127.0.0.1"
DNS_PORT = 5000

last_primary_hb = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((BACKUP_IP, BACKUP_PORT))
sock.settimeout(1)

print("Backup running... current state = STANDBY")

while True:
    try:
        data, addr = sock.recvfrom(1024)
        msg = data.decode()

        print(f"RECV from {addr}: {msg}")

        if msg.startswith("HB|PRIMARY|"):
            last_primary_hb = time.time()
            print(f"PRIMARY heartbeat received at {last_primary_hb}")

        elif msg.startswith("REQ|"):
            _, client_ip, client_port, text = msg.split("|", 3)

            response = text.upper()

            send_msg = f"RESP|{client_ip}|{client_port}|{response}"
            sock.sendto(send_msg.encode(), (DNS_IP, DNS_PORT))

            print(f"SENT to DNS: {send_msg}")

    except socket.timeout:
        pass