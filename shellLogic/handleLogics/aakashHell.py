import os

from Endpoints import Endpoints
from Plugin import Plugin
from argparse import ArgumentParser
from rich.console import Console
from rich.table import Table
from glv import Global
from userPrefs import PreferencesLoader
import base64

from utils.Utils import Utils

def download_asset(topic):
    Global.sprint(f"Topic is valid!")
    # topic = response[0]['data']
    console = Console()

    license = topic['license']

    # base64 decode this license
    license = base64.b64decode(license).strip().decode('utf-8')
    url = topic['url']

    import requests
    response = requests.get(url)

    # get file name
    enc_file_name = Utils.safe_file_name(url.split('/')[-1]).replace(".pdf", ".enc.pdf")
    file_name = Utils.safe_file_name(url.split('/')[-1])
    with open(enc_file_name, "wb") as f:
        f.write(response.content)

    Utils.remove_pdf_password(enc_file_name, file_name, license)

    os.remove(enc_file_name)


class AakashCLI(Plugin):
    def __init__(self):
        from glv_var import vars, PREFS_FILE

        pf = PreferencesLoader(verbose=False)
        prefs = pf.prefs

        access_token = prefs["access_token"]
        client_id = prefs["client_id"]
        self.eps = Endpoints(
            access_token=access_token,
            client_id=client_id
        )
        super().__init__()
        self.add_command("dl", "Download aakash's pdf !", r'dl', self.hell)
        self.register_commands()

    def hell(self, args):

        parser = ArgumentParser(
            description="Download aakash's pdf"
        )

        parser.add_argument("-P", "--package", help="Package ID", type=str)
        parser.add_argument("-C", "--subject", help="Subject ID", type=str)
        parser.add_argument("-U", "--unit", help="Unit ID", type=str)
        parser.add_argument("-T", "--topic", help="Topic ID", type=str)
        parser.add_argument("--all","-A", help="Download all the pdfs", action="store_true")

        args = parser.parse_args(args)
        # if only package is provided
        if args.package and not args.subject and not args.unit and not args.topic:
            response = self.eps.PACKAGES().fetch()
            if response[1] == 200:
                Global.sprint(f"Package is valid!")
                packages = response[0]
                console = Console()
                table = Table(title="Packages", width=Global.term_col() - 20)
                table.add_column("ID")
                table.add_column("Name")
                table.add_column("Courses")
                for package in packages:

                    nested_table = Table(title="Packages")
                    nested_table.add_column("ID")
                    nested_table.add_column("Subject")
                    for course in package.courses:
                        nested_table.add_row(
                            str(course.id),
                            course.name
                        )

                    table.add_row(
                        str(package.id),
                        package.name,
                        nested_table
                    )
                console.print(table)
            else:
                Global.errprint(f"Package is invalid!")
                exit(1)

        # if package and subject is provided
        elif args.package and args.subject and not args.unit and not args.topic:
            response = self.eps.CHAPTERS(args.package, args.subject).fetch()
            if response[1] == 200:
                Global.sprint(f"Subject is valid!")
                subject = response[0]
                console = Console()

                console.print(subject.to_console_table())
            else:
                Global.errprint(f"Subject is invalid!")
                exit(1)

        # if chapter is also provided
        elif args.package and args.subject and args.unit and not args.topic:
            response = self.eps.CHAPTER(args.package, args.subject, args.unit).fetch()
            if response[1] == 200:
                Global.sprint(f"Unit is valid!")
                unit = response[0]
                console = Console()

                console.print(unit.to_console_table())

                if args.all:
                    for topic in unit.topics:
                        response = self.eps.ASSET(args.package, args.subject, args.unit, topic.id).fetch()
                        if response[1] == 200:
                            download_asset(response[0]['data'])
                        else:
                            Global.errprint(f"Topic is invalid!")
                            exit(1)
            else:
                Global.errprint(f"Unit is invalid!")
                exit(1)

        elif args.package and args.subject and args.unit and args.topic:
            response = self.eps.ASSET(args.package, args.subject, args.unit, args.topic).fetch()
            if response[1] == 200:
                download_asset(response[0]['data'])

            else:
                Global.errprint(f"Topic is invalid!")
                exit(1)
