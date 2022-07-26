"""
Main file to handle controlling of when to pull and compile, talks to compileHandler, gitHandler and processes config

London
"""
from src.Compile import Compile
from src.Git import Git

from src.Config import *

import socket
import os

""" Port to look for webhook call"""
PORT = 1337


def main() -> int:
    """
    Handle running on webhook call
    """
    cmdList, postCompileBinPath, binFinalLoc = process_compile("cfg/compile.xml")
    repoLink, branch, repoPath = process_git("cfg/git.xml")

    gh = Git(repoLink, branch, repoPath)
    ch = Compile(cmdList, repoPath, postCompileBinPath, binFinalLoc)

    headDir = os.getcwd()

    while True:
        s = socket.socket()

        s.bind((socket.gethostname(), PORT))
        s.listen(2)
        print("Waiting for connection...")
        conn, _ = s.accept()
        _ = conn.recv(1024)
        conn.close()

        # Now execute
        execute(gh, ch)

        os.chdir(headDir)

    return 0


def execute(gh, ch):
    """
    Handle running the program
    """
    if gh.update():
        ch.compile()
        print("Compilation done!")


if __name__ == "__main__":
    main()
