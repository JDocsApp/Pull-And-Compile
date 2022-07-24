"""
File to handle processing the configuration settings

London
"""
import xml.etree.ElementTree as ET


def process_compile(path: str) -> tuple[str]:
    """
    Processes the compile settings from the xml file

    :param path: Path to xml file
    :return: Tuple of commands to run
    """
    xmlFile = ET.parse(path)
    rootNode = xmlFile.getroot()
    cmdNode = rootNode.find("CommandList")

    # Loop through and append to a list
    cmdList = []
    for command in cmdNode.iter("Command"):
        if command.text is not None:
            cmdList.append(command.text)

    return tuple(cmdList)


def process_git(path: str) -> tuple[str, str, str]:
    """
    Processes the git settings from the xml file

    :param path: Path to xml file
    :return: String of repo link, branch, String of path to store repo
    """
    xmlFile = ET.parse(path)
    rootNode = xmlFile.getroot()

    repoNode = rootNode.find("Repo")
    branchNode = rootNode.find("Branch")
    repoPathNode = rootNode.find("RepoPath")

    repo = ""
    if repoNode.text is not None:
        repo = repoNode.text
    else:
        raise Exception("No repository name specified. Check git.xml")

    branch = ""
    if branchNode.text is not None:
        branch = branchNode.text
    else:
        raise Exception("No branch name specified. Check git.xml")

    if repoPathNode.text is not None:
        return repo, branch, repoPathNode.text
    else:
        raise Exception("No repo storing location specified. Check git.xml")

