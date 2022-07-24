"""
Runs all the commands associated with pulling and talking to the repo, checking for changes

London
"""
import os
import subprocess


class Git:
    def __init__(self, repoLink: str, branch: str, storePath: str):
        self.repoLink = repoLink
        self.branch = branch
        self.storePath = storePath

        self.setupComplete = os.path.isdir(storePath)

    def setup_repo(self) -> None:
        """
        Setup the repo

        :throws: If setup was unsuccessful
        """
        os.system("rm -rf {}".format(self.storePath))

        if os.system("mkdir {}".format(self.storePath)) != 0:
            raise Exception("Failed to make dir at {}".format(self.storePath))

        os.chdir("{}".format(self.storePath))

        os.system("git clone {} .".format(self.repoLink))
        os.system("git checkout {}".format(self.branch))

        os.system("git pull")

        self.setupComplete = True

    def test_pull(self) -> bool:
        """
        Fetch into the temp location and determine changes

        :return: If there are actually changes
        """
        os.chdir("{}".format(self.storePath))
        hasChanges = subprocess.check_output(["git", "fetch"]).decode() != ""

        return hasChanges

    def update(self) -> bool:
        """
        Checks for changes and pulls them if needed

        :return: If there were changes
        """
        if not self.setupComplete:
            self.setup_repo()
            return False

        if not self.test_pull():
            return False

        # Otherwise pull changes, this resets as well to make sure the changes are properly pulled
        os.system("git reset --hard")
        os.system("git checkout {}".format(self.branch))
        os.system("git pull --force")

        return True
