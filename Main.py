"""
Main file to handle controlling of when to pull and compile, talks to compileHandler, gitHandler and processes config

London
"""
from src.Compile import Compile
from src.Git import Git

from src.Config import *


def main() -> int:
    cmdList, postCompileBinPath, binFinalLoc = process_compile("cfg/compile.xml")
    repoLink, branch, repoPath = process_git("cfg/git.xml")

    gh = Git(repoLink, branch, repoPath)
    ch = Compile(cmdList, repoPath, postCompileBinPath, binFinalLoc)

    if gh.update():
        ch.compile()
        print("Compilation done!")

    return 0


if __name__ == "__main__":
    main()
