def dictionary_attack(target_password, dictionary_file):
    attempts = 0

    try:
        with open(dictionary_file, 'r') as file:
            for line in file:
                guess = line.strip()
                attempts += 1
                if guess == target_password:
                    print(f"Password found: '{guess}' after {attempts} attempts.")
                    return guess
    except FileNotFoundError:
        print(f"Dictionary file '{dictionary_file}' not found.")
        return None

    print("Password not found in dictionary.")
    return None


if __name__ == "__main__":
    # Example target password to `c`rack
    target = "password123"

    # Path to your dictionary file (one password per line)
    dictionary_file = "common.txt" #replace with rock you or your own dictionary file 

    dictionary_attack(target_password=target, dictionary_file=dictionary_file)
