import sys
import os
import fileinput
import argparse
from shutil import copy

parser = argparse.ArgumentParser()
parser.add_argument("repo", help="path of the repo to be analyzed")
parser.add_argument("logger", help="full path of logger script")
args = parser.parse_args()

dir = args.repo
dirToAPI = args.logger


def appendTabs(indexOfDef):
    output = ""
    if indexOfDef == 4:
        return "\t\t"
    elif indexOfDef == 0:
        return "\t"
    elif indexOfDef % 4 != 0:
        return output
    else:
        time = indexOfDef / 4
        for i in range(0, time + 1):
            output += "\t"

    return output


def injectToContents(content):
    importline = "import loggerAPI\n"
    fromline = "from loggerAPI import startlog, log, f\n"
    startlogline = "startlog()\n"
    starterContent = fromline + importline + startlogline + content
    lines = starterContent.splitlines()

    newLines = []

    for line in lines:
        indexOfDef = line.find("def ")
        newLines.append(line)
        if indexOfDef > -1:
            logline = appendTabs(indexOfDef)
            logline += "log()\n"
            logline += appendTabs(indexOfDef)
            logline += "f.count()"

            newLines.append(logline)

    newContent = ""

    for line in newLines:
        newLine = line + "\n"
        newContent += newLine
    return newContent


def injectToFile(pathToFile):
    f = open(pathToFile, "r")
    content = f.read()
    content2 = injectToContents(content)

    print(content2)

    f = open(pathToFile, "w")
    f.write(content2)
    f.close()


def tabsToSpaces(pathToFile):
    inputFile = open(pathToFile, "r")
    content = inputFile.read()
    inputFile.close()
    lines = content.splitlines()
    exportFile = open(pathToFile, "w")
    for line in lines:
        # replace each tab with 4 spaces
        new_line = line.replace("\t", "    ")
        exportFile.write(new_line + "\n")
    exportFile.close()


excluded_files = ["loggerAPI.py"]
# Main part of the script
# traverses the dir specified above, and finds the python files and calls the inject code
for root, dirs, files in os.walk(dir):
    path = root.split(os.sep)
    for file in files:
        if file.endswith(".py") and file not in excluded_files:
            pathToFile = root + "/" + file
            injectToFile(pathToFile)
            tabsToSpaces(pathToFile)


# need to copy the api file to the directory
copy(dirToAPI, dir)
