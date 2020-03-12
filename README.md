# Final-Project-Crypto

# Theoretical Questions

## 1. How to safely store the passwords?

The fact is that storing the passwords in a **plain-text field is very unsecure** because it's very easy for a hacker to get them. Storing the representation of a password in the database is the proper thing to do. That means **to hash the password using a salt** (which should be different for every user) **and a secure one-way algorithm** and store that, throwing away the original password. Then, when you want to verify a password, you hash the value (using the same hashing algorithm and salt) and compare it to the hashed value in the database.

Indeed, the danger with simply hashing a password and storing that is that if a trespasser gets a hold of your database, he can still use what are known as rainbow tables to be able to "decrypt" the password. To get around this, developers add a salt to passwords which, when properly done, makes rainbow attacks simply infeasible to do. 

## 2. Which type of encryption we should use in the implementation? Why? What if we use some simple encryption like AES-CBC?
