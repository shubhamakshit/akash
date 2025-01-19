import os
from glv import Global

vars = {

    # $script is the path to the folder containing the pwdl.py file
    # Since the userPrefs.py is in the startup folder,
    # we need to go one level up however we make the exception that if the pwdl.py is in the same folder as
    # the startup folder, we don't need to go one level up
    "$script": os.path.dirname(__file__)
}
env_file = os.getenv('AAKASH_PREF_FILE')
if env_file and os.path.exists(env_file):
    print(f"Using preferences file: {env_file}")
    PREFS_FILE = env_file
else:
    Global.errprint(f"Using default preferences file: {os.path.join(vars['$script'], 'defaults.json')}")
    PREFS_FILE = os.path.join(vars["$script"], 'defaults.json')

