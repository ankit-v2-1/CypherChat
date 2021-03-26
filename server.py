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
port = 12345
so.bind((host, port))
print(colored("[+] server is live..", "green"))


so.listen(5)
print(colored("[+] waiting for connection..", 'green'))
c, addr = so.accept()

print("[+] connected to ", addr)

password = input(colored("Enter the password: ", 'red'))

hash = SHA256.new()
hash.update(password.encode('utf-8'))
hkey = hash.digest()


while True:
    message = input('send: ')
    message = encrypt(message)
    c.send(message)
    print(colored("typing..", 'green'))
    message = c.recv(1024)
    message = decrypt(message)
    print("rev: ", message)
