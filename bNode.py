import socket
from Crypto.Cipher import AES
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 2222))
key3 = b'1111111111111111'
iv = b'2222222222222222'

msg = client.recv(4096)
if msg.decode() == "CBC":
    optiune = "CBC"
else:
    optiune = "OFB"
print("1. Optiunea este: " + optiune)

client.send(b"2. B a inceput comunicarea")

msg = client.recv(4096)
msg2 = str(msg)
print("2. B a primit cheia criptata:  " + msg2)

def decripteazakey(x):
    global key3
    decipher = AES.new(key3, AES.MODE_ECB)
    cheiedecriptata = decipher.decrypt(x)
    return cheiedecriptata

cheie = decripteazakey(msg)
val2 = str(cheie)
print("3. B a decriptat cheia: " + val2)

def cripteazaiv(cheie, iv):
    cipher = AES.new(cheie, AES.MODE_ECB)
    ivcriptat = cipher.encrypt(iv)
    return ivcriptat

def shiftiv(ivcriptat,iv):
    stanga = ivcriptat[:8]
    dreapta = iv[8:]
    iv = stanga + dreapta
    return iv

def decripteazaCBC( blocinformatie, blocanterior, cheie):
    decipher = AES.new(cheie, AES.MODE_ECB)
    blocdecriptat =  decipher.decrypt(blocanterior)
    blocmod = bytes([_a ^ _b for _a, _b in zip(blocdecriptat, blocinformatie)])
    print(" - Decriptarea: " + str(blocmod))

def decripteazaOFB(blocinformati,ivcriptat):
    blocinformatie = blocinformati[:8]
    blociv = ivcriptat[:8]
    plaintext = bytes([_a ^ _b for _a, _b in zip(blociv, blocinformatie)])
    print(" - Decriptarea: " + str(plaintext))

def decrypt_iv(cheie, iv):
    decipher = AES.new(cheie, AES.MODE_ECB)
    blocdecriptat = decipher.decrypt(iv)
    return blocdecriptat


msg = client.recv(4096)
blocanterior = msg
msg = client.recv(4096)
ivcriptat = cripteazaiv(cheie,iv)

while len(msg) == 16:
    msg2 = str(msg)
    print(" + Primit blocul: " + msg2)

    if optiune == "CBC":
        decipher = AES.new(cheie, AES.MODE_ECB)
        blocdecriptat = decipher.decrypt(blocanterior)
        blocmod = bytes([_a ^ _b for _a, _b in zip(blocdecriptat, msg)])
        print(" - Decriptarea: " + str(blocmod))
        blocanterior = msg

    else:
        decripteazaOFB(msg,ivcriptat)
        iv = decrypt_iv(ivcriptat, iv)
        ivcriptat = cripteazaiv(cheie, iv)
    msg = client.recv(4096)


