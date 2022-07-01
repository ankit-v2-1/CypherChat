import socket
from termcolor import colored


from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def encrypt(info):
    msg = info
    BLOCK_SIZE = 16
    PAD = "{"
    def padding(s): return s+(BLOCK_SIZE-len(s)) % BLOCK_SIZE*PAD
    cipher = AES.new(hkey, AES.MODE_ECB)
    result = cipher.encrypt(padding(msg).encode('latin-1'))
    return result


def decrypt(info):
    msg = info
    PAD = "{"
    decipher = AES.new(hkey, AES.MODE_ECB)
    pt = decipher.decrypt(msg).decode('latin-1')
    pad_index = pt.find(PAD)
    result = pt[:pad_index]
    return result


so = socket.socket()
host = socket.gethostname()
port = 8000

so.connect((host, port))
print(colored("[+] connected to the server..", 'green'))

password = input(colored("Set the key/password: ", 'red'))

hash_obj = SHA256.new(password.encode('utf-8'))
hkey = hash_obj.digest()


while True:
    print(colored("listening..", 'green'))
    message = so.recv(1024)
    message = decrypt(message)
    print("rec: ", message)
    message = input('send: ')
    message = encrypt(message)
    so.send(message)
