import socket
import sys
from common import *


def read_hns_table(which):
    hns_table = list()
    for line in open(which, 'r'):
        hns_table.append(line.rstrip("\n\r"))

    return hns_table


def parse_line(line):
    key, chall, host = line.split(" ")
    return key, chall, host


def clear_output_file():
    with open("RESOLVED.txt", 'w') as file:
        file.write("")


# read PROJ3-HNS.txt

def main():

    # what the client sends to the server
    requests = [parse_line(line) for line in read_hns_table("PROJ3-HNS.txt")]

    # Define the port on which you want to connect to the AS server
    PORT = 65000
    # get local hostname
    HOST = socket.gethostbyname(sys.argv[1]) if len(sys.argv) > 1 else socket.gethostbyname('localhost')

    for key, chall, host in requests:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as auth_s:
                # authenticate
                print("Contacting auth server...")
                auth_s.connect((HOST, PORT))
                print("Success.")
                digest = make_digest(key, chall)
                auth_s.sendall(pack(digest + " " + chall))
                response = unpack(auth_s.recv(packet_size))
                print(response)
                tlds_name,tlds_port = response.split(" ")
                tlds_port = int(tlds_port)
                # Contact DNS server
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tlds_s:
                        print("Contacting " + tlds_name + " TLDS...")
                        tlds_s.connect((tlds_name, tlds_port))
                        tlds_s.sendall(pack(host))
                        response = unpack(tlds_s.recv(packet_size))
                        with open("RESOLVED.txt", 'a') as file:
                            if str(response) != "ERROR: HOST NOT FOUND":
                                response = str(response)[1:-1]
                            file.write(str(response) + "\n")
                except ConnectionRefusedError:
                        print("Error: Unable to contact TLDS server. Exiting...")

        except ConnectionRefusedError:
            print("Error: Unable to contact auth server. Did you run as.py first?")
            print("Exiting...")
            break
if __name__ == "__main__":
    clear_output_file()
    main()

