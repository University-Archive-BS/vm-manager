import hashlib

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = " "

    def login(self, username, password):
        if self.username == username and self.password == password:
            token = hashlib.md5(f"{username}::{password}".encode())
            self.token = token.hexdigest()
            return token.hexdigest()
        else:
            return False

    def check_token(self, token):
        if self.token == token:
            return True
        else:
            return False
    
    def is_admin(self, token):
        if self.check_token(token) and self.username == "admin":
            return True
        else:
            return False