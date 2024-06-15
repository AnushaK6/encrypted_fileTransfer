import socket
import os
from Crypto.Cipher import AES
import rsa

FILE="file"
#FILE="vid.mp4"

with open("public.pem","rb") as f:
    public_key=rsa.PublicKey.load_pkcs1(f.read())

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(("192.168.29.239", 9999))

key=b"AESEncryptionKey"
nonce=b"AESEncryptionKey"

rsa_key=rsa.encrypt(key, public_key)
client.send(rsa_key+b"<KEY>")
cipher=AES.new(key,AES.MODE_EAX,nonce)

file_name="file.txt<SEP>".encode()
# msg=cipher.encrypt(msg)
file_size=os.path.getsize(FILE)
client.send(file_name)
client.send((str(file_size)+"<SEP>").encode())

with open(FILE,"rb") as f:
    data=f.read()

encrypted=cipher.encrypt(data)

client.sendall(encrypted)
client.send(b"<END>")

f.close()
client.close()