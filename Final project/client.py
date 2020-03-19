from spake2 import SPAKE2_A
from pwn import *
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import pandas as pd 
import json
from cryptography.fernet import Fernet

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend





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
        self.df = df # dataframe
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
                     salt=None, info=infoA.encode('utf-8'), backend=backend)
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
        # TODO: transfer amount of money from your balance to to.

        nonce = os.urandom(16)
        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode=None, backend=default_backend())
        encryptor = cipher.encryptor()
        request = encryptor.update(json.dumps({
        'sender': self,
        'receiver': to,
        'amount': amount
        }))

        self.send(request)
        status = self.recv()
        self.close()
        return status

    def ask_account(self, accountNumber, amount):
        num=0
        Lacc=[]
        Lmon=[]
        ind=1
        for i in range(self.df.shape(0)):
            if self.username == self.df.loc(i, self.username):
                Lacc[i] = self.df.loc(i, accountNumber)
                Lmon[i] = self.df.loc(i, amount)

                num+=1
        acc=Lacc[0]
        if num>1:
            print("please chose from these account wich one you would like to use:<\n")
            while num >0:
                print("Choix "+str(ind)+" =>Compte n°: "+str(Lacc[num-1])+" , amount avaible : "+str(Lmon[num-1]))
                num=num-1
                ind=ind+1
            no=input()
            acc=Lacc[len(Lacc-no)]
        return(acc)

    def checkBalance(self, accountNumber, amount):
        a = self.df[(self.df['AccountNumber'] == accountNumber) & (self.df['Balance'] >= amount)] # Row of sender A

        if not a.empty:
            return True, a
        else:
            return False, a

    def checkId(self):
        a = self.df[(self.df['Email'] == self.username) & (self.df['Password'] == self.password)] # Row of sender A

        if not a.empty:
            return True, a
        else:
            return False, a

    def checkSender(self, user, accountSender):
        a = user[user['AccountNumber'] == accountSender]
        print(a)

        if not a.empty:
            return True
        else:
            return False

    def updateDataset(self, a, to, amount):

        c = self.df[self.df['AccountNumber'] == to] # Row of receiver C

        self.df.loc[a.index[0], 'Balance'] -= amount
        self.df.loc[c.index[0], 'Balance'] += amount
        print(self.df)
        self.df.to_csv('result.txt', header=None, index=None, sep=',', mode='a')

        return self.df


if __name__ == "__main__":
    username = df.loc[1, 'Email']
    password = df.loc[1, 'Password']
    client = Client(username, password)
    client.connect(host, port)

    accountSender = 'A002'
    amount = 28

    correctId, user = client.checkId()
    print(user)

    if correctId:
        if client.checkSender(user, accountSender):
            valid, a = client.checkBalance(accountSender, amount)

            if valid:
                df = client.updateDataset(a, 'B001', amount)
    
   
    status = client.transfer(receiver, 999)
    print(status)
