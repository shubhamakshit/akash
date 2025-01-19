from shellLogic.handleLogics.aakashHell import AakashCLI
from shellLogic.handleLogics.HandleCMDUtils import HandleBasicCMDUtils

from Plugin import Plugin

AakashCLI()
HandleBasicCMDUtils()

def execute_help(command, args=[]):
    Plugin().help(command)

def execute(command, args=[]):
    Plugin().parseAndRun(command, args)