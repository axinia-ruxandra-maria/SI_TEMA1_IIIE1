import socket
import json
from Crypto.Cipher import AES
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('127.0.0.1', 2222))
serv.listen(5)
key3 = b'1111111111111111'
iv = b'2222222222222222'

def read_json(nume):
    with open(nume) as f:
     data = json.load(f)
    return data

def cripteazacheie(cheie):
    global iv
    key = cheie
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(iv)
    return ciphertext

def cripteazaprimulbloc(blocinformatie, iv, cheie):
    blocmod = bytes([_a ^ _b for _a, _b in zip(blocinformatie, iv)])
    cipher = AES.new(cheie, AES.MODE_ECB)
    ciphertext = cipher.encrypt(blocmod)
    return ciphertext

def cripteazaCBC(blocinformatie,blocanterior, cheie):
    blocmod = bytes([_a ^ _b for _a, _b in zip(blocinformatie, blocanterior)])
    cipher = AES.new(cheie, AES.MODE_ECB)
    ciphertext = cipher.encrypt(blocmod)
    return ciphertext

def decripteazakey(x):
    global key3
    decipher = AES.new(key3, AES.MODE_ECB)
    cheiedecriptata = decipher.decrypt(x)
    return cheiedecriptata

def cripteazaiv(cheie, iv):
    cipher = AES.new(cheie, AES.MODE_ECB)
    ivcriptat = cipher.encrypt(iv)
    return ivcriptat

def cripteazablocfinalcipertext(blocinformatie, ivcriptat):
    bitiplaintext = blocinformatie[:8]
    biticipertext = ivcriptat[:8]
    blocfinalcipertext = bytes([_a ^ _b for _a, _b in zip(bitiplaintext, biticipertext)])
    blocfinalcipertext = blocfinalcipertext + b'}}}}}}}}'
    return blocfinalcipertext

def ivrecursiv(ivcriptat, iv):
    dreapta = ivcriptat[:8]
    stanga = iv[8:]
    iv = stanga + dreapta
    return iv



conn, addr = serv.accept()

#am luat optiunea in fisier pt modul de operare generat aleatoriu de main.py
optiune = read_json("optiune.json")
if optiune == 1:
    conn.send(b"CBC")
    optiune = "CBC"
else:
    conn.send(b"OFB")
    optiune = "OFB"

#salvam cheia generata de keymanager.py si salvata in fisier
file_in = open("encrypted.bin", "rb")
cheie = file_in.read(16)

#trimitem cheia catre B
conn.send(cheie)

#decriptam cheia
cheie = decripteazakey(cheie)
val2 = str(cheie)
print("1. A a decriptat cheia: "+ val2)

#asteptam confirmarea de la B
mesaj = conn.recv(4096)


if len(mesaj) > 0:

    print(mesaj.decode())

    if optiune == "CBC":

        file_in = open("fisier.bin", "rb")

        #citim blocuri de informatie din fisierul de input

        blocinformatie1 = file_in.read(16)
        blocanterior = cripteazaprimulbloc(blocinformatie1, iv, cheie)

        while file_in:
            blocinformatie = file_in.read(16)
            bloccriptat = cripteazaCBC(blocinformatie,blocanterior, cheie)
            conn.send(cripteazaCBC(blocinformatie,blocanterior, cheie))
            blocanterior = bloccriptat

    else:
         file_in = open("fisier.bin", "rb")
         ivcriptat = cripteazaiv(cheie,iv)

         while file_in:

             blocinformatie = file_in.read(16)


             blocfinalcipertext = cripteazablocfinalcipertext(blocinformatie, ivcriptat)
             conn.send(blocfinalcipertext)

             iv = ivrecursiv(iv,blocinformatie)
             ivcriptat = cripteazaiv(cheie, iv)



conn.close()
