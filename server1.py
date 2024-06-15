import socket
import tqdm
import rsa
from Crypto.Cipher import AES


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("192.168.29.239", 9999))
server.listen()

client, addr=server.accept()



with open("private.pem","rb") as f:
    private_key=rsa.PrivateKey.load_pkcs1(f.read())

recvd=client.recv(1024)
# print(recvd.split(b"<KEY>"))
rsa_key=recvd.split(b"<KEY>")[0]
# print(rsa_key)
key=rsa.decrypt(rsa_key, private_key)
nonce=key

cipher=AES.new(key,AES.MODE_EAX,nonce)


recvd=recvd.split(b"<KEY>")[1]
# print(f"recvd:{recvd}")
if recvd=="":
    recvd=client.recv(1024)
msg=recvd.decode("utf-8", "ignore")
# print(msg.split("<SEP>"))
# file_name=cipher.decrypt(file_name)
file_name=msg.split("<SEP>")[0]
file_size=msg.split("<SEP>")[1]

if file_size=="":
    recvd=client.recv(1024)
    msg=recvd.decode("utf-8", "ignore")
    file_size=msg.split("<SEP>")[0]
    data=recvd[len(file_size)+5:]

else:
    data=recvd[len(file_name)+len(file_size)+10:]

file=open(file_name,"wb")

done=False
file_bytes=b""

progress=tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(file_size))

while not done:
   
    if file_bytes[-5:]==b"<END>":
        done=True
    else:
        file_bytes+=data
    progress.update(1024)
    data=client.recv(1024)

decrypted=cipher.decrypt(file_bytes[:-5])
file.write(decrypted)

file.close()
client.close()
server.close()