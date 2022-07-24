"""
Main file to handle controlling of when to pull and compile, talks to compileHandler, gitHandler and processes config

London
"""
from src.Compile import Compile
from src.Git import Git

from src.Config import *


def main() -> int:
    cmdList = process_compile("cfg/compile.xml")
    repo = process_git("cfg/git.xml")

    ch = Compile(["test"])
    gh = Git("github.com")

    print("Hello World!")
    return 0


if __name__ == "__main__":
    main()
