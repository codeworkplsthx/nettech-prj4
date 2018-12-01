import socket
import sys
from common import *


def read_hns_table(which):
    hns_table = list()
    for line in open(which, 'r'):
        hns_table.append(line.rstrip("\n\r"))

    return hns_table

def parse_line(line):
    key,chall,host = line.split(" ")
    return key,chall,host

def clear_output_file():
    with open("RESOLVED.txt", 'w') as file:
        file.write("");
#read PROJ3-HNS.txt

def main():
    # what the client sends to the server
    requests = [parse_line(line) for line in read_hns_table("PROJ3-HNS.txt")]

    # Define the port on which you want to connect to the AS server
    PORT = 65000
    # get local hostname
    HOST = socket.gethostbyname('localhost')

    for key,chall,host in requests:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as auth_s:
                #authenticate
                auth_s.connect((HOST, PORT))
                digest = make_digest(key,chall)
                auth_s.sendall(pack(digest + " " + chall))
                tlds_name = unpack(auth_s.recv(packet_size))

                #Contact DNS server
                if tlds_name in tlds_map:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tlds_s:
                        print("Contacting " + tlds_name + " TLDS...")
                        tlds_s.connect(('localhost', tlds_map.get(tlds_name)))
                        tlds_s.sendall(pack(host))
                        response = unpack(tlds_s.recv(packet_size))
                        with open("RESOLVED.txt", 'a') as file:
                                file.write(str(response) + "\n")
                else:
                    print("Invalid TLDS hostname returned to client: " + tlds_name + "exiting...")
                    break

        except ConnectionRefusedError:
            print("Error: Unable to contact auth server. Did you run as.py first?")
            break





if __name__ == "__main__":
    clear_output_file()
    main()




'''

                if tlds_name == "com":
                    print("Contacting com TLDS...")
                    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as tlds_s:
                        tlds_s.connect(('localhost',com_port))
                        tlds_s.sendall(pack(host))
                        responses.append(unpack(tlds_s.recv(packet_size)))
                elif tlds_name == "edu":
                    print("Contacting edu TLDS...")
                    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as tlds_s:
                        tlds_s.connect(('localhost',edu_port))
                        tlds_s.sendall(pack(host))
                        responses.append(unpack(tlds_s.recv(packet_size)))
  #write DNS lookups to file
    with open("RESOLVED.txt",'w') as file:
        for resp in responses:
            file.write(str(resp) + "\n")

'''