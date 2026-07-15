from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

password = "hunter2"


hash = ph.hash(password)

try:
    ph.verify(hash, password)
    print("Password is correct")

except VerifyMismatchError:
    print("Password is not correct")