"""
Main file to handle controlling of when to pull and compile, talks to compileHandler, gitHandler and processes config

Matt
"""
from src.CompileHandler import CompileHandler
from src.GitHandler import GitHandler


def main() -> int:
    ch = CompileHandler(["test"])
    gh = GitHandler("github.com")

    print("Hello World!")
    return 0


if __name__ == "__main__":
    main()
