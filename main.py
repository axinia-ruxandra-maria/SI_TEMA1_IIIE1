import socket
import random
import json

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('127.0.0.1', 2222))
serv.listen(5)

key3 = b'1111111111111111'
iv = b'2222222222222222'

def write_json(sir, nume):
    obj = open(nume, 'wb')
    obj.write(sir)
    obj.close

#generam modul in care dorim sa fie criptate blocurile, 1-CBC, 2-OFB
lista = [1,2]
random.shuffle(lista)
a = lista[0]

if a == 1:
    conn, addr = serv.accept()
    conn.send(b"Key 1 requested")
    write_json(b'1',"optiune.json")
    #am scris in fisier de unde va citi keymanager optiunea
else:
    conn, addr = serv.accept()
    conn.send(b"Key 2 requested")
    write_json(b'2', "optiune.json")

conn.close()
