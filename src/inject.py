import sys
import os
from shutil import copy
import fileinput

# print ("directory file:", str(sys.argv[1]))

dir = "/Users/mike/Documents/School/sixth/first/CPSC410/demoProject/tetris_game"
dirToAPI = "/Users/mike/Documents/School/sixth/first/CPSC410/Project/CPSC410_Visualization/src/loggerAPI.py"


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
    fromline = "from loggerAPI import startlog, endlog, log\n"
    startlogline = "startlog()\n"
    starterContent = importline + fromline + startlogline + content
    lines = starterContent.splitlines()

    newLines = []

    for line in lines:
        indexOfDef = line.find("def ")
        newLines.append(line)
        if indexOfDef > -1:
            logline = appendTabs(indexOfDef)
            logline += "log()"
            newLines.append(logline)

    newContent = ""

    for line in newLines:
        newLine = line + "\n"
        newContent += newLine

    newContent += "\n" + "endlog()"
    return newContent


def injectToFile(pathToFile):
    f = open(pathToFile, "r")
    content = f.read()
    content2 = injectToContents(content)

    print(content2)

    f = open(pathToFile, "w")
    f.write(content2)
    f.close()


# Main part of the script
# traverses the dir specified above, and finds the python files and calls the inject code
for root, dirs, files in os.walk(dir):
    path = root.split(os.sep)
    for file in files:
        if file.endswith(".py"):
            pathToFile = root + "/" + file
            injectToFile(pathToFile)

# need to copy the api file to the directory
copy(dirToAPI, dir)
