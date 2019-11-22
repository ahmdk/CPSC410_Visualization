import sys
import os
import fileinput
import argparse
from shutil import copy
from itertools import islice

def_pos = None
def_flag = False


def window(seq, n=2):
    """Sliding window iterator."""
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


parser = argparse.ArgumentParser()
parser.add_argument("repo", help="path of the repo to be analyzed")
parser.add_argument("logger", help="full path of logger script")
args = parser.parse_args()

dir = args.repo
dirToAPI = args.logger


def appendTabs(indexOfReturn):
    output = ""
    if indexOfReturn == 4:
        return "\t\t"
    elif indexOfReturn == 0:
        return "\t"
    elif indexOfReturn % 4 != 0:
        return output
    else:
        time = indexOfReturn / 4
        for i in range(0, int(time) + 1):
            output += "\t"

    return output

def appendReturnTabs(indexOfDef):
    output = ""
    if indexOfDef == 4:
        return "\t"
    elif indexOfDef == 0:
        return ""
    elif indexOfDef % 4 != 0:
        return output
    else:
        time = indexOfDef / 4
        for i in range(0, int(time)):
            output += "\t"

    return output


def injectToContents(content):
    importline = "import loggerAPI\n"
    fromline = "from loggerAPI import t\n"
    starterContent = fromline + importline + content
    lines = starterContent.splitlines()

    newLines = []

    last_two_lines = lines[-2:]

    global def_pos
    global def_flag

    for curr, _next, far_next in window(lines, 3):
        newLines.append(curr)
        index_of_def = curr.find("def ")

        if index_of_def > -1:
            def_pos = index_of_def
            start_log_line = appendTabs(index_of_def)
            start_log_line += "t.start_timer()\n"
            newLines.append(start_log_line)
            def_flag = True

        if (def_pos != None) and (_next.find("return") > -1):
            return_pos = _next.find("return")
            end_log_line = appendReturnTabs(return_pos)
            end_log_line += "t.end_timer()\n"
            newLines.append(end_log_line)
            if return_pos == def_pos:
                def_flag = False

        if (def_pos != None) and (far_next.lstrip().find("def ") > -1) and (curr.find("return") == -1) \
                and def_flag:
            end_log_line = appendTabs(def_pos)
            end_log_line += "t.end_timer()\n"
            newLines.append(end_log_line)
            def_flag = False

        if (def_pos != None) and (_next.lstrip().find("def ") > -1) and def_flag:
            end_log_line = appendTabs(def_pos)
            end_log_line += "t.end_timer()\n"
            newLines.append(end_log_line)
            def_flag = False

        if (def_pos != None) and (_next == '') and (far_next == '') and def_flag:
            end_log_line = appendTabs(def_pos)
            end_log_line += "t.end_timer()\n"
            newLines.append(end_log_line)
            def_flag = False

    newContent = ""

    for line in newLines:
        newLine = line + "\n"
        newContent += newLine

    for line in last_two_lines:
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
