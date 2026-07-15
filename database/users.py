users = {}

def get_user(username):
    return users.get(username)

def add_user(username, hashed_password):
    if username in users:
        return False  
    users[username] = {
        "username": username, 
        "password": hashed_password
        }
    return True