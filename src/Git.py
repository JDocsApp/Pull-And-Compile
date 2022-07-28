"""
Runs all the commands associated with pulling and talking to the repo, checking for changes

"""
import os
import subprocess

from src.Logger import Logger


class Git:
    def __init__(self, repoLink: str, branch: str, storePath: str, logger: Logger):
        """
        Constructor for Git object

        :param repoLink: Link to repository
        :param branch: Branch to pull
        :param storePath: Place to store repo
        :param logger: Logger to print and save to file
        """
        self.repoLink = repoLink
        self.branch = branch
        self.storePath = storePath
        self.logger = logger

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
        self.logger.log("Looking for changes...")
        os.chdir("{}".format(self.storePath))
        os.system("git checkout {} 2> /dev/null > /dev/null".format(self.branch))
        os.system("git fetch 2> /dev/null > /dev/null")
        hasChanges = False
        try:
            hasChanges = "behind" in subprocess.check_output(["git", "status"]).decode().split("\n")[1]
        except:
            hasChanges = False

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
            self.logger.log("No changes have been made.")
            return False

        self.logger.log("Changes have been made.")
        self.logger.log("Pulling..")

        # Otherwise pull changes, this resets as well to make sure the changes are properly pulled
        os.system("git reset --hard > /dev/null")
        os.system("git checkout {} > /dev/null".format(self.branch))
        os.system("git pull --force > /dev/null")

        self.logger.log("Pulled successsfully")

        return True
