"""
Runs all commands associated with compiling and checking for successful compile

London
"""
import os


class Compile:
    def __init__(self, cmds: list[str]):
        """
        Constructor for creating the handler

        :param cmds:
        """
        self.cmds = cmds

    def run_compile(self) -> bool:
        """
        Runs all compilation steps unless one fails. Returns true if all are successful, false otherwise

        :return: If compilation was successful
        """
        for cmd in self.cmds:
            res = os.system("{} > /dev/null".format(cmd))
            if res != 0:
                return False

        return True
