import bcrypt


password = b"hunter2" #b shows that password is stored in bytes
#make a salt
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)
print("Bcrypt hash:", hashed)

#verify hash and password
if bcrypt.checkpw(password, hashed):
    print("Password all g")
else:  
    print("Password is not it sonion")