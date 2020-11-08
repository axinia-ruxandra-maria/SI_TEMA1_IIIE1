import socket
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 2222))


#generam aleatoriu valorile pt key1 si key2
key1 = get_random_bytes(16) #CBC
key2 = get_random_bytes(16)#OFB

#key3 si iv sunt aceleasi si in aNode si bNode, detinute din start
key3 = b'1111111111111111'
iv = b'2222222222222222'

def write_json(sir, nume):
    obj = open(nume, 'wb')
    obj.write(sir)
    obj.close

def cripteaza(val,cheie):
    #keymanager cripteaza si scrie cheia in fisier pentru ca aNode.py o va prelua
    file_out = open("encrypted.bin", "wb")
    cipher = AES.new(cheie, AES.MODE_ECB)
    criptat = cipher.encrypt(val)
    file_out.write(criptat)
    file_out.close()

msg = client.recv(4096)

if msg.decode() == "Key 1 requested":
    criptat = cripteaza(key1,key3)

else:
    criptat = cripteaza(key2,key3)

client.close()


