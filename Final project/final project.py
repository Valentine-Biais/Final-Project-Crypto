import pandas as pd 
import numpy as np

def main():
    # import the full dataset
    df = pd.read_csv('database.txt', names = ['Email', 'Password', 'AccountNumber', 'Balance']) # dataframe
    print(df)

    accountSender = 'A002'

    correctId, user = checkId(df, 'A', 123456)
    print(user)

    if correctId:
        if checkSender(user, accountSender):
            valid, a = checkBalance(df, accountSender, 28)

            if valid:
                df = updateDataset(df, a, 'B001', 28)

def checkBalance(df, accountNumber, amount):

    a = df[(df['AccountNumber'] == accountNumber) & (df['Balance'] >= amount)] # Row of sender A

    if not a.empty:
        return True, a
    else:
        return False, a

def checkId(df, email, password):

    a = df[(df['Email'] == email) & (df['Password'] == password)] # Row of sender A

    if not a.empty:
        return True, a
    else:
        return False, a

def checkSender(user, accountSender):
    a = user[user['AccountNumber'] == accountSender]
    print(a)

    if not a.empty:
        return True
    else:
        return False

def updateDataset(df, a, to, amount):

    c = df[df['AccountNumber'] == to] # Row of receiver C

    df.loc[a.index[0], 'Balance'] -= amount
    df.loc[c.index[0], 'Balance'] += amount
    print(df)
    df.to_csv('result.txt', header=None, index=None, sep=',', mode='a')

    return df

main()