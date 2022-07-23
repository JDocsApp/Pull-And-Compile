"""
Runs all the commands associated with pulling and talking to the repo, checking for changes

Matt
"""
import os


class GitHandler:
    def __init__(self, repoLink: str):
        self.repoLink = repoLink

