
class Node(object):
    def __init__(self, character, filePath):
        self.character = character
        self.members = []
        self.filePath = filePath


class Trie(object):

    def __init__(self):
        self.head = Node("", "")
        self.curNode = self.head

    def addData(self, textToAdd, fileLocation, atStart):

        if(atStart == True):  # this function will operate recursivly, we need to know if we are creating a new entry
            self.curNode = self.head
            atStart = False

        haveNextLetter = False
        # is the character to add in the set of members
        for member in self.curNode.members:
            if member.character == textToAdd[0].lower():
                # if its there, that node can no longer be associated with a unique file
                member.filePath = ""
                self.curNode = member
                haveNextLetter = True
                break

        # are we going to need to add a new characer
        if(haveNextLetter == False):
            newNode = Node(textToAdd[0].lower(), fileLocation)
            self.curNode.members.append(newNode)
            self.curNode = newNode

        textToAdd = textToAdd[1:]

        if(textToAdd == ""):
            # we have added all the needed text
            print("Entry has been added!")
        else:
            self.addData(textToAdd, fileLocation, False)

    # This is a depth first seach of the tree

    def getPossibleFiles(self, text, atStart):
        # take in a portion of a song/artist

        if(atStart == True):  # we need to traverse to the last character in the entry, then from there evaluate the possible paths
            self.curNode = self.head
            for(character in text):
                for(member in self.curNode.members):
                    if(member.character == character):

        possibleFiles = []

        for character in text:


def main():

    artistTree = Trie()

    artistTree.addData("Pink Floyd", "/Desktop/asdfasd.mp3", True)
    artistTree.addData("Pearl Jam", "/Desktop/axcvd.mp3", True)


if __name__ == "__main__":
    main()
