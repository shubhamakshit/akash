from Plugin import Plugin


class AakashCLI(Plugin):
    def __init__(self):
        super().__init__()
        self.add_command("hell", "Hell with World!", r'hell', self.hell)
        self.register_commands()

    def hell(self, args):
        print("Hell with World! ", args)