import shutil

from rich.console import Console
from rich.table import Table

import shell
from Endpoints import Endpoints
from glv import Global
from sudat import SudoLogin
from userPrefs import PreferencesLoader
from glv_var import vars, PREFS_FILE

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

Global.sprint(f"Checking if user is valid...")
# response = user.fetch()

# if response[1] == 200:
#     Global.sprint(f"User is valid!")
#     packages = response[0]
#     import json



#     #Global.dprint(json.dumps(packages, indent=4))
# else:
#     Global.errprint(f"User is invalid!")
#     exit(1)


def TitleCase(string):
    return string[0].upper() + string[1:]

# table = Table(title="Packages")
# for attr in packages[0].__dict__().keys():
#     table.add_column(TitleCase(attr))
#
# for package in packages:
#
#     nested_courses_table = Table(title="Courses")
#     courses = package.courses
#     for course in courses:
#         nested_courses_table.add_row(
#             str(course.id),
#             course.slug,
#             course.name
#         )
#
#     table.add_row(
#         str(package.id),
#         package.name,
#         nested_courses_table
#     )
#
# console.print(table)








def main():
    shell.main()


if __name__ == '__main__':
    main()
