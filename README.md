# Final-Project-Crypto 

# Theoretical Questions

## 1. How to safely store the passwords?

  The fact is that storing the passwords in a **plain-text field is very unsecure** because it's very easy for a hacker to get them. Storing the representation of a password in the database is the proper thing to do. That means **to hash the password using a salt** *(which should be different for every user)* **and a secure one-way algorithm** and store that, throwing away the original password. Then, when you want to verify a password, you hash the value *(using the same hashing algorithm and salt)* and compare it to the hashed value in the database.

Indeed, the danger with simply hashing a password and storing that is that if a trespasser gets a hold of your database, he can still use what are known as rainbow tables to be able to "decrypt" the password. To get around this, developers add a salt to passwords which, when properly done, makes rainbow attacks simply infeasible to do. 

## 2. Which type of encryption we should use in the implementation? Why? What if we use some simple encryption like AES-CBC?

  The first question we must ask ourselves is the following:
- *Should we use a **Symmetric or Asymetric** encryption?*
To answer this question, we need to know if both the server and the client have access to the same secret key. If they do, we can implement a symmetric encryption. If not, we use a Asymmetric encryption.
In this case, if the PAKE protocol succeeds, both the client and the server know the secret key so we can use a symmetric type of encryption. 
Thus we can use a AES 128 or AES 256 encryption and it so happens that that is the encryption that banks use to secure their date and transactions.

Also, we want to use an authenticated encryption. That's why we should not use AES-CBC. Indeed, **CBC is not an authenticated encryption mode**. Any unauthenticated encryption is theoretically vulnerable to Chosen Ciphertext Attacks (CCA), and in the case of CBC that isn’t just “theoretical”. CBC isn't as parallelizable as GCM for instance and lacks built-in authentication. Due to this, CBC is only really practical for encrypting local files that don't need random access.

> BIAIS Valentine ; KEBRAT Erwan ; HARAJ TOUZANI Younes ; RIEUL Thibault
