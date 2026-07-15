import string

passwd = input("Enter the target password(max 8 characters): ")

def brute_force(target_password, max_length=8):
    chars = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
    attempts = [0]  # use list to make it mutable in nested scope

    def try_password(current):
        if len(current) > max_length:
            return None

        # Check if current guess matches
        if current == target_password:
            attempts[0] += 1
            print(f"Password found: '{current}' after {attempts[0]} attempts.")
            return current

        # Keep adding one more character
        for c in chars:
            attempts[0] += 1
            result = try_password(current + c)
            if result:
                return result

        return None

    # Start with empty string
    result = try_password("")
    if not result:
        print("Password not found.")

if __name__ == "__main__":
    target = passwd
    brute_force(target_password=target, max_length=8)
