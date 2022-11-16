import socket
import argparse

parser=argparse.ArgumentParser(description="Server script to echo to a client")
parser.add_argument("--port",default=5000,type=int,help="Port you would like to open for communication.")
args=parser.parse_args()
port=args.port;

while True:
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.settimeout(0.25)
    active=True
    server.bind(('',port))
    server.listen()
    try:
        client,addr=server.accept()
        print("Client: IP "+str(addr[0])+" Port "+str(addr[1]))
        while(active):
            frame=client.recv(1024)
            active=len(frame)>0
            if(active):
                client.sendall(frame)
                print(frame.decode('ascii'))
            else:
                print("Client disconnected!")
    except:
        pass