#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True # Suppress .pyc files
import pronouncing as pr
import random
from creative_ai.pysynth import pysynth
from creative_ai.utils.menu import Menu
from creative_ai.data.dataLoader import *
from creative_ai.models.musicInfo import *
from creative_ai.models.languageModel import LanguageModel

TEAM = 'Glasses'
LYRICSDIRS = ['country_all']
TESTLYRICSDIRS = ['the_beatles_test']
MUSICDIRS = ['gamecube']
WAVDIR = 'wav/'

def output_models(val, output_fn = None):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  outputs the dictionary val to the given filename. Used
              in Test mode.

    This function has been done for you.
    """
    from pprint import pprint
    if output_fn == None:
        print("No Filename Given")
        return
    with open('TEST_OUTPUT/' + output_fn, 'wt') as out:
        pprint(val, stream=out)

def sentenceTooLong(desiredLength, currentLength):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  returns a bool indicating whether or not this sentence should
              be ended based on its length.

    This function has been done for you.
    """
    STDEV = 1
    val = random.gauss(currentLength, STDEV)
    return val > desiredLength

def printSongLyrics(verseOne, verseTwo, chorus):
    """
    Requires: verseOne, verseTwo, and chorus are lists of lists of strings
    Modifies: nothing
    Effects:  prints the song.
    
    This function is done for you.
    """
    verses = [verseOne, chorus, verseTwo, chorus]

    for verse in verses:
        for line in verse:
            print((' '.join(line)).capitalize())
        print()

def trainLyricModels(lyricDirs, test=False):
    """
    Requires: lyricDirs is a list of directories in data/lyrics/
    Modifies: nothing
    Effects:  loads data from the folders in the lyricDirs list,
              using the pre-written DataLoader class, then creates an
              instance of each of the NGramModel child classes and trains
              them using the text loaded from the data loader. The list
              should be in tri-, then bi-, then unigramModel order.
              Returns the list of trained models.
              
    This function is done for you.
    """
    model = LanguageModel()

    for ldir in lyricDirs:
        lyrics = prepData(loadLyrics(ldir))
        model.updateTrainedData(lyrics)

    return model

def trainMusicModels(musicDirs):
    """
    Requires: musicDirs is a list of directories in data/midi/
    Modifies: nothing
    Effects:  works exactly as trainLyricsModels, except that
              now the dataLoader calls the DataLoader's loadMusic() function
              and takes a music directory name instead of an artist name.
              Returns a list of trained models in order of tri-, then bi-, then
              unigramModel objects.
              
    This function is done for you.
    """
    model = LanguageModel()

    for mdir in musicDirs:
        music = prepData(loadMusic(mdir))
        model.updateTrainedData(music)

    return model

def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """

    userWord = input('Enter the word: ')
    phrase = models.generatePhrase(userWord)
    print('Phrase:')
    print(phrase)

    verseOne = generateMusicForPhrase(models, userWord, phrase);

    print()
    for line in verseOne:
        print((' '.join(line)).capitalize())
    print()

def generateMusicForPhrase(models, userWord, phrase):
    """
    Requires: models is a list of a trained nGramModel child class objects.
              phrase is a word that the new song should be generated base on
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """

    verseOne = []
    verseOne.append(generateTokenSentence(models, 7, phrase, userWord, True))

    #getting the first two last words for rhyming
    line1 = generateTokenSentence(models, 7, phrase, userWord)
    while len(pr.rhymes(line1[-1])) == 0:
        line1 = generateTokenSentence(models, 7, phrase, userWord)
    rhyme_list_1 = pr.rhymes(line1[-1])
    
    line2 = generateTokenSentence(models, 7, phrase, userWord)
    while len(pr.rhymes(line2[-1])) == 0:
        line2 = generateTokenSentence(models, 7, phrase, userWord)
    rhyme_list_2 = pr.rhymes(line2[-1])

    verseOne.append(line1)
    verseOne.append(line2)
    if rhyme_list_1 == []:
        rhyme_list_1 = None
    verseOne.append(generateTokenSentence(models, 7, phrase, userWord, False, rhyme_list_1))
    if rhyme_list_2 == []:
        rhyme_list_2 = None
    verseOne.append(generateTokenSentence(models, 7, phrase, userWord, False, rhyme_list_2))
    verseOne.append(generateTokenSentence(models, 7, phrase, userWord, True))

    return verseOne;

def runMusicGenerator(models, songName):
    """
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  uses models to generate a song and write it to the file
              named songName.wav
    """

    verseOne = []
    verseTwo = []
    chorus = []

    for i in range(4):
        verseOne.extend(generateTokenSentence(models, 7))
        verseTwo.extend(generateTokenSentence(models, 7))
        chorus.extend(generateTokenSentence(models, 9))

    song = []
    song.extend(verseOne)
    song.extend(verseTwo)
    song.extend(chorus)
    song.extend(verseOne)
    song.extend(chorus)

    pysynth.make_wav(song, fn=songName)

###############################################################################
# Begin Core >> FOR CORE IMPLEMENTION, DO NOT EDIT OUTSIDE OF THIS SECTION <<
###############################################################################

def generateTokenSentence(model, desiredLength, phrase, userWord, start=False, filter=None):
    """
    Requires: models is a list of trained NGramModel objects sorted by
              descending priority: tri-, then bi-, then unigrams.
              desiredLength is the desired length of the sentence.
              phrase is a three word string
    Modifies: nothing
    Effects:  returns a list of strings where each string is a word in the
              generated sentence. The returned list should NOT include
              any of the special starting or ending symbols.

              For more details about generating a sentence using the
              NGramModels, see the spec.
    """
    
    newSentence = []
    nextToken = ""
    if start:
        newSentence = [phrase]
        nextToken = model.getNextToken(['^::^', '^:::^', newSentence[0]])
    else:
        nextToken = model.getNextToken(['^::^', '^:::^'])
    
    while((not sentenceTooLong(desiredLength, len(newSentence))) and (nextToken != '$:::$')):
        newSentence.append(nextToken)
        nextToken = model.getNextToken(newSentence, None)

    #placing the phrase
    for index, val in enumerate(newSentence):
        if val is userWord:
            newSentence[index] = phrase

    #putting rhyme words at the end of each sentence
    if filter is not None and filter is not []:
        if len(newSentence) not in [0, 1]:
            oldWord = newSentence[-1]
            del newSentence[-1]
            
            nextToken = model.getNextToken(newSentence, filter)
            if nextToken == '$:::$':
                nextToken = oldWord
            newSentence.append(nextToken)

    return newSentence


###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

PROMPT = [
    'Generate country song lyrics',
    'Generate a song using data from Nintendo Gamecube',
    'Run twitter processor',
    'Quit the music generator'
]

def main():
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  This is your main function, which is done for you. It runs the
              entire generator program for both the reach and the core.

              It prompts the user to choose to generate either lyrics or music.
    """

    mainMenu = Menu(PROMPT)

    lyricsTrained = False
    musicTrained = False

    print('Welcome to the {} music generator!'.format(TEAM))
    while True:
        userInput = mainMenu.getChoice()

        if userInput == 1:
            if not lyricsTrained:
                print('Starting lyrics generator...')
                lyricsModel = trainLyricModels(LYRICSDIRS)
                lyricsTrained = True

            runLyricsGenerator(lyricsModel)

        elif userInput == 2:
            if not musicTrained:
                print('Starting music generator...')
                musicModel = trainMusicModels(MUSICDIRS)
                musicTrained = True

            songName = input('What would you like to name your song? ')
            
            runMusicGenerator(musicModel, WAVDIR + songName + '.wav')

        elif userInput == 3:            
            if not lyricsTrained:
                lyricsModel = trainLyricModels(LYRICSDIRS)
                lyricsTrained = True

            from creative_ai.twitter import TwitterManager
            print('Starting twitter tracker...')
            tm = TwitterManager("xyrR5WQJO5v1ZhKicBOJGrlKj", "KrqzS5VWkpM3rmAmQmVZbpRnHRCOMuTgtetCU7ZSzIk1GxKD4c", "1070065717796634631-YYrAWPS8TJoDVSrvcj2HVyNqaBesmE", "JOJiIuGZRtv27nE5oZLXsISOFTqdjbsLZq7VDlCqcMn14", lyricsModel)

        elif userInput == 4:
            print('Thank you for using the {} music generator!'.format(TEAM))
            sys.exit()

# This is how python tells if the file is being run as main
if __name__ == '__main__':
    main()
    # note that if you want to individually test functions from this file,
    # you can comment out main() and call those functions here. Just make
    # sure to call main() in your final submission of the project!
