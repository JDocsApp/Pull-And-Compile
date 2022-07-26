"""
Runs all commands associated with compiling and checking for successful compile

"""
import os

from src.Logger import Logger

class Compile:
    def __init__(self, cmds: tuple[str], repoPath: str, compiledPath: str, finalLocation: str, logger: Logger):
        """
        Constructor to build the compile object

        :param cmds: List of commands to run to compile
        :param repoPath: Path to where the repo is stored
        :param compiledPath: Path to the binary after it is compiled
        :param finalLocation: Where to save the binary when build success
        :param logger: Logger to print and save to file
        """
        self.cmds = cmds
        self.repoPath = repoPath
        self.compiledPath = compiledPath
        self.finalLocation = finalLocation
        self.logger = logger

    def run_compile(self) -> bool:
        """
        Runs all compilation steps unless one fails. Returns true if all are successful, false otherwise

        :return: If compilation was successful
        """
        os.chdir(self.repoPath)

        self.logger.log("Compiling..")

        for cmd in self.cmds:
            self.logger.log("Running: {}".format(cmd))
            # Check if this command is to change directories
            path = ""
            chdir = False
            if "cd" in cmd:
                chdir = True
                path = cmd.split()[1]

            res = 0
            if chdir:
                os.chdir(path)
            else:
                res = os.system("{} > /dev/null".format(cmd))

            if res != 0:
                self.logger.log("Command failed... Exiting")
                return False

        self.logger.log("Compile successful")
        return True

    def move_binary(self) -> bool:
        """
        Moves the binary into the correct location

        :return: If the move is successful
        """
        self.logger.log("Moving binary..")
        res = os.system("mv {} {}".format(self.compiledPath, self.finalLocation))
        return res == 0

    def compile(self) -> bool:
        """
        Function that handles the compilation and moving assuming compilation was successful

        :return: If the compilation was successful
        """
        if self.run_compile():
            if self.move_binary():
                return True

        return False
