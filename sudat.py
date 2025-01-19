from glv import  Global
class SudoLogin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        Global.sprint(f"Logging in as {self.username}...")
