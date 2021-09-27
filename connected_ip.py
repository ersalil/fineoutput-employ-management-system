from scapy.all import ARP, Ether, srp
import socket

def get_ips():
    own_ip = socket.gethostbyname(socket.gethostname())
    print("own_ip : ", type(own_ip))
    own_ip = own_ip + "/24"
    print(own_ip)
    # target_ip = "192.168.0.4/24"
    target_ip = own_ip
    arp = ARP(pdst=target_ip)

    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=0)[0]
    clients = []
    for sent, received in result:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})

    return clients

