"""
Main file to handle controlling of when to pull and compile, talks to compileHandler, gitHandler and processes config

London
"""
from src.Compile import Compile
from src.Git import Git

from src.Config import *

import socket

""" Port to look for webhook call"""
PORT = 1337


def main() -> int:
    """
    Handle running on webhook call
    """
    s = socket.socket()

    while True:
        s.bind(("localhost", PORT))
        s.listen(2)
        conn, addr = s.accept()
        _ = conn.recv(1024)
        conn.close()

        # Now execute
        execute()

    return 0


def execute():
    """
    Handle running the program
    """
    cmdList, postCompileBinPath, binFinalLoc = process_compile("cfg/compile.xml")
    repoLink, branch, repoPath = process_git("cfg/git.xml")

    gh = Git(repoLink, branch, repoPath)
    ch = Compile(cmdList, repoPath, postCompileBinPath, binFinalLoc)

    if gh.update():
        ch.compile()
        print("Compilation done!")


if __name__ == "__main__":
    main()
