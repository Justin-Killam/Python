import socket
import argparse

parser=argparse.ArgumentParser(description="Client script to send a command to a server and read its response")
parser.add_argument("--ip",default="127.0.0.1",help="IP address of the server you would like to connect to.")
parser.add_argument("--port",default=5000,type=int,help="Port on the server side you would like to connect to.")
args=parser.parse_args()
ip=args.ip
port=args.port

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect((ip,port))
print("Sending: Hi")
server.sendall(b'Hi')
frame=server.recv(1024)
print("Recieve: "+frame.decode('ascii'))
server.close()


