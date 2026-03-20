import socket
import time

BACKUP_IP = "127.0.0.1"
BACKUP_PORT = 5002

DNS_IP = "127.0.0.1"
DNS_PORT = 5000

TIMEOUT = 3
last_primary_hb = time.time()
primary_alive = True
backup_state = "STANDBY"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((BACKUP_IP, BACKUP_PORT))
sock.settimeout(1)

print(f"Backup running... current state = {backup_state}")

while True:
    current_time = time.time()

    if primary_alive and current_time - last_primary_hb > TIMEOUT:
        print("PRIMARY TIMEOUT DETECTED (BACKUP)")
        primary_alive = False
        backup_state = "ACTIVE"
        print(f"BACKUP STATE = {backup_state}")

    try:
        data, addr = sock.recvfrom(1024)
        msg = data.decode()

        print(f"RECV from {addr}: {msg}")

        if msg.startswith("HB|PRIMARY|"):
            last_primary_hb = time.time()
            primary_alive = True
            print(f"PRIMARY heartbeat received at {last_primary_hb}")

        elif msg.startswith("REQ|"):
            if backup_state == "ACTIVE":
                _, client_ip, client_port, text = msg.split("|", 3)

                response = text.upper()

                send_msg = f"RESP|{client_ip}|{client_port}|{response}"
                sock.sendto(send_msg.encode(), (DNS_IP, DNS_PORT))

                print(f"SENT to DNS: {send_msg}")
            else:
                print("IGNORING REQUEST: backup is still STANDBY")

    except socket.timeout:
        pass