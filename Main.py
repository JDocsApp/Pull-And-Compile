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
        conn, pl = s.accept()
        pl = conn.recv(1024)
        conn.close()

        # Now execute
        if (validate_signature(pl,"1vXf!53jrjHc")):
            execute(gh, ch)
            os.chdir(headDir)


    return 0

def validate_signature(payload, secret):

    # Get the signature from the payload
    signature_header = payload['headers']['X-Hub-Signature']
    sha_name, github_signature = signature_header.split('=')
    if sha_name != 'sha1':
        print('ERROR: X-Hub-Signature in payload headers was not sha1=****')
        return False
      
    # Create our own signature
    body = payload['body']
    local_signature = hmac.new(secret.encode('utf-8'), msg=body.encode('utf-8'), digestmod=hashlib.sha1)

    # See if they match
    return hmac.compare_digest(local_signature.hexdigest(), github_signature)

def execute(gh, ch):
    """
    Handle running the program
    """
    if gh.update():
        ch.compile()
        print("Compilation done!")


if __name__ == "__main__":
    main()
