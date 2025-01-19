import shell
from Endpoints import Endpoints
from sudat import SudoLogin
from userPrefs import PreferencesLoader

pf = PreferencesLoader(verbose=False)
prefs = pf.prefs


access_token = prefs["access_token"]
client_id = prefs["client_id"]


# check if user is valid
eps = Endpoints(
    access_token=access_token,
    client_id=client_id
)

user = eps.PACKAGES()

from argparse import ArgumentParser

parser = ArgumentParser(description="A command line interface for the Aakash API")

parser.add_argument("-v", "--version", action="store_true", help="Print the version of the CLI")
parser.add_argument("--login", action="store_true", help="Login to the Aakash API")

args = parser.parse_args()

if args.login:
    sdlogin = SudoLogin()
    sdlogin.login()

def main():
    shell.main()


if __name__ == '__main__':
    main()
