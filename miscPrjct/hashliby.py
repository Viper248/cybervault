import hashlib


password = input("Enter password sonion: ") 
salt = "xyz123"
salt = "" #for no salt uncomment 
combined_password = password + salt
print("Original password: ", password)
print("Combined password: ", combined_password)

#MD5
md5_hash = hashlib.md5(combined_password.encode()).hexdigest()
print("MD5 Hash: ", md5_hash)

#sha256
sha256_hash = hashlib.sha256(combined_password.encode()).hexdigest()
print("SHA256 Hash: ", sha256_hash)

