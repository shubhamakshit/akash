from shellLogic.handleLogics.aakashHell import AakashCLI
from Plugin import Plugin

AakashCLI()

def execute_help(command, args=[]):
    Plugin().help(command)

def execute(command, args=[]):
    Plugin().parseAndRun(command, args)