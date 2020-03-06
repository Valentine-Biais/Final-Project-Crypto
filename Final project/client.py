from spake2 import SPAKE2_A
from pwn import *
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import pandas as pd 

# import the full dataset
df = pd.read_csv('database.txt', names = ['Email', 'Password', 'AccountNumber', 'Balance']) # dataframe
print(df)

# some constants
InfoBank = b"confirm_Bank"
host = 'localhost'
port = 9999


username = b'A'
password = b'12345678'
receiver = b'B'


class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connection = None

    def connect(self, host, port):
        self.connection = remote(host, port)
        self.send(self.username)

    def send(self, msg):
        self.connection.sendline(msg)
    
    def recv(self):
        return self.connection.recvline().rstrip()

    def close(self):
        self.connection.close()

    def handshake(self):
        backend = default_backend()
        infoA = self.username
        hkdfA = HKDF(algorithm=hashes.SHA256(), length=32,
                     salt=None, info=infoA, backend=backend)
        hkdfB = HKDF(algorithm=hashes.SHA256(), length=32,
                     salt=None, info=InfoBank, backend=backend)
        hs = SPAKE2_A(self.password)
        msg_out = hs.start()
        self.send(msg_out)  # this is message A->B
        msg_in = self.recv()
        key = hs.finish(msg_in)
        confirm_A = hkdfA.derive(key)
        expected_confirm_B = hkdfB.derive(key)
        self.send(confirm_A)
        confirm_B = self.recv()
        assert confirm_B == expected_confirm_B
        return key

    def transfer(self, to, amount):
        secretKey = self.handshake()
        print(secretKey.hex())
        # TODO: transfer `amount` of money from your balance to `to`.


        status = self.recv()
        self.close()
        return status

    
    def checkBalance(self, accountNumber, amount):

        a = df[(df['AccountNumber'] == accountNumber) & (df['Balance'] >= amount)]
        print(a)

        if not a.empty:
            return True
        else:
            return False


if __name__ == "__main__":
    username = df.loc[1, 'Email']
    password = df.loc[1, 'Password']
    client = Client(username, password)
    client.checkBalance('A002', 28)
    client.connect(host, port)
    status = client.transfer(receiver, 999)
    print(status)
