import json

from rich.console import Console
from glv_var import PREFS_FILE
from update import UpdateJSONFile
from glv import  Global
from Endpoints import Endpoints



class SudoLogin:


    def login(self):
        eps = Endpoints(None)

        console = Console()

        console.print("Enter your username and password to login",style="bold green")

        username = input("Username: ")
        password = input("Password: ")



        response = eps.LOGIN(username, password).fetch()

        Global.dprint(
            json.dumps(response[0], indent=4)
        )

        if response[1] == 200:
            Global.sprint("Login successful!")
            access_token = response[0]['data']["access_token"]

            u = UpdateJSONFile(PREFS_FILE)
            u.update("access_token", access_token)
            Global.sprint("Access token updated!")



        else:
            Global.errprint("Login failed!")
            exit(1)
