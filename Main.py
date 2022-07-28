"""
Main file to handle controlling of when to pull and compile, talks to compileHandler, gitHandler and processes config

"""
from src.Compile import Compile
from src.Git import Git
from src.Logger import Logger
from src.Config import *

import socket
import os

""" Port to look for webhook call"""
PORT = 1337


def main() -> int:
    """
    Handle running on webhook call
    """
    logger = Logger("Log.txt")

    cmdList, postCompileBinPath, binFinalLoc = process_compile("cfg/compile.xml")
    repoLink, branch, repoPath = process_git("cfg/git.xml")

    gh = Git(repoLink, branch, repoPath, logger)
    ch = Compile(cmdList, repoPath, postCompileBinPath, binFinalLoc, logger)

    headDir = os.getcwd()

    while True:
        s = socket.socket()

        s.bind((socket.gethostname(), PORT))
        s.listen(2)
        logger.log("Waiting for connection...")
        conn, _ = s.accept()
        pl = conn.recv(1024).decode()
        conn.close()

        # Now execute
        if execute(gh, ch, logger):
            os.chdir(headDir)

            # If anything else needs to happen with services after compilation, do that here


    return 0


def execute(gh, ch) -> bool:
    """
    Handle running the program
    """
    if gh.update():
        ch.compile()
        print("Compilation done!")
        return True
    return False


if __name__ == "__main__":
    main()
