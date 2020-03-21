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

    return output


def getArtistFromFile(file_name):
    commandToRun = 'ffprobe -loglevel error -show_entries format_tags=artist -of default=noprint_wrappers=1:nokey=1 '
    commandToRun += file_name
    process = subprocess.run(commandToRun, shell=True, check=True,
                             stdout=subprocess.PIPE, universal_newlines=True, cwd=PATH_TO_MP3)

    return process.stdout


def playSong(file_name):
    commandToRun = "ffplay "
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
        self.lastCharInSong = False


class Trie(object):

    def __init__(self):
        self.head = Song("", "", "", "", "")
        self.possibleSongs = []  # possible songs will contain song objects

    '''
        function: addSong (Recursive)

        input: textToAdd, fileLocation, atStart

        purpose: adds a string of characters into the tree
    '''

    def addSong(self, songToAdd, current_song):

        haveNextLetter = False
        # is the character to add in the set of members
        for member in current_song.members:

            if member.character == songToAdd.buffer[0].lower():
                # we could write after a song that contains a filepath
                if(not member.lastCharInSong):
                    member.filePath = ""
                    member.song_name = ""
                    member.song_artist = ""
                current_song = member
                haveNextLetter = True
                break

        # are we going to need to add a new element to the tree, meaning a unique song
        if(haveNextLetter == False):
            newSong = Song(buffer="", character=songToAdd.buffer[0].lower(),
                           filePath=songToAdd.filePath,  song_title=songToAdd.song_title, song_artist=songToAdd.song_artist)

            current_song.members.append(newSong)
            current_song = newSong

        # if last character, designate this as end of data so we know not to overwrite its filepath
        if(len(songToAdd.buffer) == 1):
            current_song.lastCharInSong = True

        songToAdd.buffer = songToAdd.buffer[1:]

        if(songToAdd.buffer == ""):
            # we have added all the needed text
            print("Successfully added: {}".format(songToAdd.song_title))
        else:
            self.addSong(songToAdd, current_song)

    '''
        function: traverseAllPaths (Recursive)

        input: the song to start from, atStart representss if we are doing a new search

        purpose: add possible filePaths to list

    '''

    def traverseAllPaths(self, songObject):

        # if we find a filepath that isnt designated as the last song, we dont have to go any further
        if(songObject.filePath != ''):
            self.possibleSongs.append(songObject)
            if(not songObject.lastCharInSong):
                return

        for member in songObject.members:
            self.traverseAllPaths(member)

        return

    '''
        function: getpossibleSongs

        input: song intance to begin search from

        purpose: return possible files based on user entry then call traverseAllPaths to find all possible files after that

    '''

    def getpossibleSongs(self, searchTerm):
        self.possibleSongs.clear()
        text = searchTerm.lower()

        current_song = self.head

        '''
        First deal with the given text.
        Traverse the tree until the last character
        If there is a filepath at any song that is the only result we need to look for
        '''

        while (len(text) != 0):

            foundCharacter = False
            for member in current_song.members:
                if(member.character.lower() == text[0]):
                    foundCharacter = True
                    if(member.filePath != ""):
                        # if we reach a filepath we only need to continue the search if the node is not marked as lastCharInSong
                        self.possibleSongs.append(member)

                        if(not member.lastCharInSong):
                            print("Only 1 song matches the input")
                            return

                    current_song = member

            if(foundCharacter == False):
                return "No Results"

            text = text[1:]

        '''
        now add the 'auto complete' results

        depth first search from where the given text left us

        '''

        self.traverseAllPaths(current_song)

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

            self.addSong(songToAdd, self.head)


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

            i = 0
            for song in dataTree.possibleSongs:
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print("Song {}".format(i + 1))
                print("Title: {} \nArtist: {} \nFilePath: {}\n Search completed in {} seconds.".format(
                    song.song_title, song.song_artist, song.filePath, t_stop - t_start))
                i += 1
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('\n')

            response = input("Would you like to play a song? (y/n)")

            if(response.lower() == "y"):
                response = int(input("Which song number?"))

                playSong(dataTree.possibleSongs[response - 1].filePath)
                print("\n \n")


if __name__ == "__main__":
    main()
