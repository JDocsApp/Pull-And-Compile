"""
Runs all commands associated with compiling and checking for successful compile

Matt
"""
import os


class CompileHandler:
    def __init__(self, cmds: list[str]):
        self.cmds = cmds

