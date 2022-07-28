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
        _ = conn.recv(1024)
        conn.close()

        # Now execute
        execute(gh, ch, logger)

        os.chdir(headDir)

    return 0


def execute(gh, ch, logger):
    """
    Handle running the program
    """
    if gh.update():
        ch.compile()
        logger.log("Compilation done!")


if __name__ == "__main__":
    main()
