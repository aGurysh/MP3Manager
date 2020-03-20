import os
import subprocess

'''

mp3Manager v 1.0.0

Adam Gurysh

All recursive functions take True as a third argument. Some people will hate this i think it improves code readability.

'''


PATH_TO_MP3 = "/home/adam/Desktop/MP3"


class Node(object):
    def __init__(self, character, filePath):
        self.character = character
        self.members = []
        self.filePath = filePath
        self.lastCharInData = False


class Trie(object):

    def __init__(self):
        self.head = Node("", "")
        self.curNode = self.head
        self.possibleFiles = []
        self.visitedNodes = []

    '''
        function: addData (Recursive)

        input: textToAdd, fileLocation, atStart

        purpose: adds a string of characters into the tree
    '''

    def addData(self, textToAdd, fileLocation, atStart):
        if(atStart):  # this function will operate recursivly, we need to know if we are creating a new entry
            self.curNode = self.head
            atStart = False

        haveNextLetter = False
        # is the character to add in the set of members
        for member in self.curNode.members:
            if member.character == textToAdd[0].lower():

                # we could write after a node that contains a filepath
                if(not member.lastCharInData):
                    member.filePath = ""

                self.curNode = member
                haveNextLetter = True
                break

        # are we going to need to add a new characer
        if(haveNextLetter == False):
            newNode = Node(textToAdd[0].lower(), fileLocation)
            self.curNode.members.append(newNode)
            self.curNode.members
            self.curNode = newNode

        # if last character, designate this as end of data so we know not to overwrite its filepath
        if(len(textToAdd) == 1):
            self.curNode.lastCharInData = True

        textToAdd = textToAdd[1:]

        if(textToAdd == ""):
            # we have added all the needed text
            print("Entry has been added!")
        else:
            self.addData(textToAdd, fileLocation, False)

    '''
        function: traverseAllPaths (Recursive)

        input: the node to start from, atStart representss if we are doing a new search

        purpose: add possible filePaths to list

    '''

    def traverseAllPaths(self, nodeObject, atStart):
        if(atStart):
            self.visitedNodes.clear()
            atStart = False

        if(nodeObject.filePath != ''):
            if(nodeObject.filePath not in self.possibleFiles):
                self.possibleFiles.append(nodeObject.filePath)
                self.visitedNodes.append(nodeObject)

        for member in nodeObject.members:
            if(member not in self.visitedNodes):
                self.traverseAllPaths(member, False)

        return

    '''
        function: getPossibleFiles

        input: text to search for

        purpose: return possible files based on user entry then call traverseAllPaths to find all possible files after that

    '''

    def getPossibleFiles(self, searchTerm):
        self.possibleFiles.clear()
        searchTerm = searchTerm.lower()
        text = searchTerm
        self.curNode = self.head

        '''
        First deal with the given text.
        Traverse the tree until the last character
        If there is a filepath at any node that is the only result we need to look for
        '''

        while (len(text) != 0):
            foundCharacter = False
            for member in self.curNode.members:
                if(member.character == text[0]):
                    foundCharacter = True
                    if(member.filePath != "" and member.filePath not in self.possibleFiles):
                        self.possibleFiles.append(member.filePath)

                    self.curNode = member
            if(foundCharacter == False):
                return "No Results"
            text = text[1:]

        '''
        now add the possible results 

        depth first search from where the given text left us

        '''

        self.traverseAllPaths(self.curNode, True)

        return self.possibleFiles

    '''
        function: addFiles

        input: path to directory of files

        purpose: iterate through list of files, adding them to the tree

    '''

    def addFiles(self, path_to_files):

        fileNames = os.listdir(path_to_files)

        print("adding the following files: {}".format(fileNames))

        for fileName in fileNames:
            commandToRun = 'ffprobe -loglevel error -show_entries format_tags=title -of default=noprint_wrappers=1:nokey=1 '
            commandToRun += fileName

            try:
                process = subprocess.run(
                    commandToRun, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True, cwd=path_to_files)

                output = process.stdout

                self.addData(output, fileName, True)

            except:
                print("could not get song title from file: {}".format(fileName))


def main():

    dataTree = Trie()

    dataTree.addData("Cochise", "/Desktop/cochize.mp3", True)

    dataTree.addData("Show Me How To Live", "/Desktop/showmetolive.mp3", True)

    dataTree.addData("Gasoline", "/Desktop/carJuice.mp3", True)

    dataTree.addData("What You Are", "/Desktop/whatIAm.mp3", True)

    dataTree.addData("Like a stone", "/Desktop/asArock.mp3", True)

    dataTree.addData("Set it Off", "/Desktop/setItOff.mp3", True)

    dataTree.addData("Shadow on the Sun", "/Desktop/shadow.mp3", True)

    dataTree.addFiles(PATH_TO_MP3)

    while(True):
        searchTerm = input("Enter some text to search the system: ")

        print("Here are the possible files \n")
        print(dataTree.getPossibleFiles(searchTerm))
        print("\n")


if __name__ == "__main__":
    main()
