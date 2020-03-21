import os
import subprocess
from time import process_time

'''

mp3Manager v 1.0.0

Adam Gurysh


'''


PATH_TO_MP3 = "/home/adam/Desktop/MP3"


def getSongNameFromFile(file_name):

    commandToRun = 'ffprobe -loglevel error -show_entries format_tags=title -of default=noprint_wrappers=1:nokey=1 '
    commandToRun += file_name
    process = subprocess.run(commandToRun, shell=True, check=True,
                             stdout=subprocess.PIPE, universal_newlines=True, cwd=PATH_TO_MP3)

    output = str(process.stdout).strip()

    return process.stdout


def getArtistFromFile(file_name):
    commandToRun = 'ffprobe -loglevel error -show_entries format_tags=artist -of default=noprint_wrappers=1:nokey=1 '
    commandToRun += file_name
    process = subprocess.run(commandToRun, shell=True, check=True,
                             stdout=subprocess.PIPE, universal_newlines=True, cwd=PATH_TO_MP3)

    return process.stdout


# everything is a song, if a song doesnt have a filepath, its letter is being shared by more than one song

class Song(object):
    def __init__(self, character, filePath, song_title, song_artist, buffer):
        self.character = character
        self.members = []
        self.filePath = filePath
        self.song_title = song_title
        self.song_artist = song_artist
        self.buffer = buffer
        self.lastCharInData = False


class Trie(object):

    def __init__(self):
        self.head = Song("", "", "", "", "")
        self.curSong = self.head
        self.possibleSongs = []  # possible songs will contain song objects
        self.visitedCharacters = []  # keeps track of which nodes we have visited at each leve

    '''
        function: addSong (Recursive)

        input: textToAdd, fileLocation, atStart

        purpose: adds a string of characters into the tree
    '''

    def addSong(self, songToAdd, atStart):

        if(atStart):  # this function will operate recursivly, we need to know if we are creating a new entry
            self.curSong = self.head

        haveNextLetter = False
        # is the character to add in the set of members
        for member in self.curSong.members:
            if member.character == songToAdd.buffer[0]:

                # we could write after a song that contains a filepath
                if(not member.lastCharInData):
                    member.filePath = ""
                    member.song_name = ""
                    member.song_artist = ""

                self.curSong = member
                haveNextLetter = True
                break

        # are we going to need to add a new element to the tree, meaning a unique song
        if(haveNextLetter == False):
            newSong = Song(buffer="", character=songToAdd.buffer[0],
                           filePath=songToAdd.filePath,  song_title=songToAdd.song_title, song_artist=songToAdd.song_artist)

            self.curSong.members.append(newSong)
            self.curSong = newSong

        # if last character, designate this as end of data so we know not to overwrite its filepath
        if(len(songToAdd.buffer) == 1):
            self.curSong.lastCharInData = True

        songToAdd.buffer = songToAdd.buffer[1:]

        if(songToAdd.buffer == ""):
            # we have added all the needed text
            print("Successfully added: {}".format(songToAdd.song_title))
        else:
            self.addSong(songToAdd, False)

    '''
        function: traverseAllPaths (Recursive)

        input: the song to start from, atStart representss if we are doing a new search

        purpose: add possible filePaths to list

    '''

    def traverseAllPaths(self, songObject):

        if(songObject.filePath != '' and songObject.character not in self.visitedCharacters):
            self.possibleSongs.append(songObject)
            if(not songObject.lastCharInData):  # there is no point traversing any further
                return

        self.visitedCharacters.append(songObject.character)

        for member in songObject.members:
            if(member.character not in self.visitedCharacters):
                self.traverseAllPaths(member)
                self.visitedCharacters.clear()

        return

    '''
        function: getpossibleSongs

        input: text to search for

        purpose: return possible files based on user entry then call traverseAllPaths to find all possible files after that

    '''

    def getpossibleSongs(self, searchTerm):
        self.possibleSongs.clear()
        text = searchTerm.lower()

        self.curSong = self.head

        '''
        First deal with the given text.
        Traverse the tree until the last character
        If there is a filepath at any song that is the only result we need to look for
        '''

        while (len(text) != 0):

            foundCharacter = False
            for member in self.curSong.members:
                if(member.character.lower() == text[0]):
                    foundCharacter = True
                    if(member.filePath != ""):
                        # if we reach a filepath we only need to continue the search if the node is not marked as lastCharInData
                        self.possibleSongs.append(member)

                        if(not member.lastCharInData):
                            print("Only 1 song matches the input")
                            return

                    self.curSong = member
            if(foundCharacter == False):
                return "No Results"
            text = text[1:]

        '''
        now add the possible results

        depth first search from where the given text left us

        '''

        self.traverseAllPaths(self.curSong)

    '''
        function: addFiles

        input: path to directory of files

        purpose: iterate through list of files, adding them to the tree

    '''

    def addFiles(self, path_to_files):

        filePaths = os.listdir(path_to_files)

        print("adding the following files: {}".format(filePaths))

        for filePath in filePaths:
            try:
                # for each mp3 we are going to build a song object, then pass it to self.addSong()
                artistName = getArtistFromFile(filePath)
            except:
                print("could not get artist from {}".format(filePath))

            try:
                songName = str(getSongNameFromFile(filePath))
            except:
                print("could not get song title from file: {}".format(filePath))

            songToAdd = Song(buffer=songName, character=songName[0], filePath=filePath,
                             song_title=songName, song_artist=artistName)

            self.addSong(songToAdd, True)


def main():

    dataTree = Trie()

    dataTree.addFiles(PATH_TO_MP3)

    while(True):
        searchTerm = input("Enter some text to search the system: ")

        print("Here are the possible songs: \n")

        t_start = process_time()

        if(dataTree.getpossibleSongs(searchTerm) == "No Results"):
            print("No Results")
            print("\n \n \n")
        else:
            t_stop = process_time()
            for song in dataTree.possibleSongs:
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print("Title: {} \nArtist: {} \nFilePath: {}\n Search completed in {} seconds.".format(
                    song.song_title, song.song_artist, song.filePath, t_stop - t_start))
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('\n \n \n')


if __name__ == "__main__":
    main()
