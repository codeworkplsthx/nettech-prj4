import socket
from socket import error as socket_error
from common import *
from table import Table
from dnsentry import *
import sys

HOST = ''
PORT = 65000



def main():



    com_hostname = socket.gethostbyname(sys.argv[1]) \
        if len(sys.argv)> 1 \
        else socket.gethostbyname('localhost')
    edu_hostname = socket.gethostbyname(sys.argv[2]) \
        if len(sys.argv) > 2 \
        else socket.gethostbyname('localhost')


    print("[S]: Server host name is: ", socket.gethostname())
    print("[S]: Server IP address is  ", socket.gethostbyname('localhost'))
    print("[S]: Listening on: ", PORT)

    # create portal for clients
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(PORT)

        while True:
            conn = None
            try:
                conn, addr = s.accept()
                if not conn:
                    break
                else:
                    with conn:
                        print("Got a connection request from " + str(conn.getpeername()))
                        while True:
                            # receive data from client
                            data = conn.recv(packet_size)
                            if not data:
                                break
                            else:
                                digest,chall = str2tuple(unpack(data))
                                print('Received ' + digest,chall)
                                print("Contacting com server...")
                                #connect to COM server
                                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as com:
                                    try:
                                        com.connect((com_hostname, com_port))
                                        print("Success")
                                        # send challenge string to COM server
                                        print("Sending " + chall + " to com server...")
                                        com.sendall(pack(chall))
                                        # wait for response from COM server
                                        com_digest = unpack(com.recv(packet_size))
                                        print("Received " + com_digest + " from com server")
                                    except ConnectionRefusedError:
                                        print("Can't connect to com server")
                                        com.close()
                                        break

                                # compare COM's digest to client's digest
                                # if match, return hostname of COM
                                if digest == com_digest:
                                    print("digest matches. informing client...")
                               
                                    conn.send(pack(str(com_hostname) + " " + str(com_port)))
                                else:
                                    print("digest incorrect")
                                    # connect to EDU server
                                    print("Contacting edu server...")
                                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as edu:
                                        try:
                                            edu.connect((edu_hostname, edu_port))
                                            print("Success")
                                            # send challenge string to EDU server
                                            edu.sendall(pack(chall))
                                            print("Sending " + chall + " to edu server...")
                                            # wait for response from EDU server
                                            edu_digest = unpack(edu.recv(packet_size))
                                            print("Received " + edu_digest + " from edu server")
                                        except ConnectionRefusedError:
                                            edu.close()
                                            print("Can't connect to edu server")
                                            break
                                    # compare EDU's digest to client's digest
                                    # if match, return hostname of EDU

                                    if digest == edu_digest:
                                        print("digest matches. informing client...")
                                        conn.send(pack(str(edu_hostname) + " " +str(edu_port)))
                                    else:
                                        print("digest incorrect")

            except KeyboardInterrupt:
                if conn:
                    print("Closing " + conn.getsockname())
                    conn.close()
                break



if __name__ == '__main__':
    main()

