import string
import itertools

def brute_force(target_password, max_length=4):
    chars = string.ascii_letters
    attempts = 0

    for length in range(1, max_length + 1):
        for guess_tuple in itertools.product(chars, repeat=length):
            guess = ''.join(guess_tuple)
            attempts += 1
            if guess == target_password:
                print(f"Password found: {guess} after {attempts} attempts")
                return guess
    print("Password not found.")
    return None, attempts

pswrd = input("Enter a target password: ")
target = pswrd
brute_force(target)