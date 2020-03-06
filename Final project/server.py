from spake2 import SPAKE2_B
from pwn import *
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import threading

# some constants
InfoBank = b"confirm_Bank"
host = 'localhost'
port = 9999

class Client(threading.Thread):
    def __init__(self, connection, username, password, accounts):
        threading.Thread.__init__(self)
        self.username = username
        self.password = password
        self.accounts = accounts
        self.connection = connection
    
    def __str__(self):
        return str(self.username)

    def send(self, msg):
        self.connection.sendline(msg)
    
    def recv(self):
        return self.connection.recvline().rstrip()

    def handshake(self):
        backend = default_backend()
        infoA = self.username
        infoB = InfoBank
        hkdfA = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=infoA,backend=backend)
        hkdfB = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=infoB,backend=backend)

        q = SPAKE2_B(self.password)
        msg_out = q.start()
        self.send(msg_out)
        msg_in = self.recv() # this is message A->B
        key = q.finish(msg_in)
        expected_confirm_A = hkdfA.derive(key)
        confirm_B = hkdfB.derive(key)
        self.send(confirm_B)
        confirm_A = self.recv()
        assert confirm_A == expected_confirm_A
        return key

    def transfer(self):
        status = b'OK'
        secretKey = self.handshake()
        print(secretKey.hex())
        # TODO: do your jobs here

        self.send(status)
        return status

def new_request(r):
    username = r.recvline().rstrip()
    # TODO: read from the database the corresponding accounts info
    accounts = [{'accountNumber': 0, 'balance': 0}]
    password = b'abc'

    client = Client(r, username, password, accounts)
    client.transfer()
    r.close()

if __name__ == "__main__":
    l = listen(port)
    c = l.wait_for_connection()
    new_request(c)
    c.close()
