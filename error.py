from glv import Global

errorList = {
    "cantLoadFile": {
        "code": 22,
        "func": lambda fileName: Global.errprint(f"Can't load file {fileName}"),
        "message_template": "Unable to load the file {fileName}. Check if it exists."
    },
    "couldNotMakeDir": {
        "code": 6,
        "func": lambda dirName: Global.errprint(f"Could not make directory {dirName}. Exiting..."),
        "message_template": "Unable to create the directory {dirName}. Check permissions."
    },
    "dependencyNotFound": {
        "code": 2,
        "func": lambda x=None: Global.errprint(f"{'Dependency' if x is None else x} not found. Exiting..."),
        "message_template": "{dependency} is required but was not found. Please install it."
    },
}


class AKDLError(Exception):
    def __init__(self, message, code=999, func=None, verbose=False):
        self.message = message
        self.code = code
        self.func = func
        self.verbose = verbose

        super().__init__(self.message)

    def __str__(self):
        # Color the output
        return f"Akdl Error: {self.message} Failed with code {self.code}"

    def exit(self):
        Global.errprint(self.__str__())
        exit(self.code)


class CantLoadFile(AKDLError):
    def __init__(self, fileName):
        super().__init__(errorList["cantLoadFile"]["message_template"].format(fileName=fileName),
                         errorList["cantLoadFile"]["code"],
                         errorList["cantLoadFile"]["func"])


class CouldNotMakeDir(AKDLError):
    def __init__(self, dirName):
        super().__init__(errorList["couldNotMakeDir"]["message_template"].format(dirName=dirName),
                         errorList["couldNotMakeDir"]["code"],
                         errorList["couldNotMakeDir"]["func"])


class DependencyNotFound(AKDLError):
    def __init__(self, dependency):
        super().__init__(errorList["dependencyNotFound"]["message_template"].format(dependency=dependency),
                         errorList["dependencyNotFound"]["code"],
                         errorList["dependencyNotFound"]["func"])
