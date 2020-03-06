import pandas as pd 

# import the full dataset
df = pd.read_csv('database.txt', names = ['Email', 'Password', 'AccountNumber', 'Balance']) # dataframe
print(df)

def checkBalance(accountNumber, amount):

    a = df[(df['AccountNumber'] == accountNumber) & (df['Balance'] >= amount)]
    print(a)

    if not a.empty:
        return True
    else:
        return False

def checkId(email, password):

    a = df[(df['Email'] == email) & (df['Password'] == password)]
    print(a)

    if not a.empty:
        return True
    else:
        return False

def updateDataset(self, to, amount):
    a = 0
    return a

print(checkBalance('A002', 28))
print(checkBalance('A002', 2034))