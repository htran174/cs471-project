import socket
import time

DNS_IP = "127.0.0.1"
DNS_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

print("Client running...")

while True:
    msg = "hello world"
    send_msg = f"REQ|{msg}"

    sock.sendto(send_msg.encode(), (DNS_IP, DNS_PORT))
    print(f"SENT: {msg}")

    try:
        data, _ = sock.recvfrom(1024)
        print(f"RECV: {data.decode()}")
    except socket.timeout:
        print("No response, retrying...")

    time.sleep(2)