import random
import spacy
import pronouncing as pr
from creative_ai.data.dataLoader import prepData
from creative_ai.models.unigramModel import UnigramModel
from creative_ai.models.bigramModel import BigramModel
from creative_ai.models.trigramModel import TrigramModel
from creative_ai.utils.print_helpers import key_value_pairs

class LanguageModel():

    def __init__(self, models=None):
        """
        Requires: nothing
        Modifies: self (this instance of the LanguageModel object)
        Effects:  This is the LanguageModel constructor. It sets up an empty
                  dictionary as a member variable.
        
        """

        if models != None:
            self.models = models
        else:
            self.models = [TrigramModel(), BigramModel(), UnigramModel()]

    def __str__(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  This is a string overloaded. This function is
                  called when languageModel is printed.
                  It will show the number of trained paths
                  for each model it contains. Useful for testing.
        
        """

        output_list = [
            '{} contains {} trained paths.'.format(
                model.__class__.__name__, key_value_pairs(model.nGramCounts)
                ) for model in self.models
            ]

        output = '\n'.join(output_list)

        return output

    def updateTrainedData(self, text, prepped=True):
        """
        Requires: text is a 2D list of strings
        Modifies: self (this instance of the LanguageModel object)
        Effects:  adds new trained data to each of the languageModel models.
        If this data is not prepped (prepped==False) then it is prepepd first
        before being passed to the models.

        """

        if (not prepped):
            text = prepData(text)

        for model in self.models:
            model.trainModel(text)


###############################################################################
# >> CORE IMPLEMENTION <<
###############################################################################

    def selectNGramModel(self, sentence):
        """
        Requires: self.models is a list of NGramModel objects sorted by descending
                  priority: tri-, then bi-, then unigrams.

                  sentence is a list of strings.
        Modifies: nothing
        Effects:  returns the best possible model that can be used for the
                  current sentence based on the n-grams that the models know.
                  (Remember that you wrote a function that checks if a model can
                  be used to pick a word for a sentence!)
        """
        if (self.models[0].trainingDataHasNGram(sentence)):
          return self.models[0]
        if (self.models[1].trainingDataHasNGram(sentence)):
          return self.models[1]
        
        return self.models[2]

    def weightedChoice(self, candidates):
        """
        Requires: candidates is a dictionary; the keys of candidates are items
                  you want to choose from and the values are integers
        Modifies: nothing
        Effects:  returns a candidate item (a key in the candidates dictionary)
                  based on the algorithm described in the spec.
        """
        token = []
        count = []
        for t in candidates:
            token.append(t)
            count.append(candidates[t])
        cumulative = []
        cumulative.append(count[0])
        for i in range(1, len(count)):
            cumulative.append(cumulative[i - 1] + count[i])

        randNum = random.randrange(0, cumulative[-1])
        for i in range(0, len(cumulative)):
            if (cumulative[i] > randNum): 
                return token[i]

    def getNextToken(self, sentence, filter=None):
        """
        Requires: sentence is a list of strings, and this model can be used to
                  choose the next token for the current sentence
        Modifies: sentence
        Effects:  returns the next token to be added to sentence by calling
                  the getCandidateDictionary and weightedChoice functions.
                  

                  If a filter is being used, and none of the models
                  can produce a next token using the filter, then a random
                  token from the filter is returned instead.
        """
        model = self.selectNGramModel(sentence)
        dict = model.getCandidateDictionary(sentence)
        if filter is None:
            return self.weightedChoice(dict)
        else:
            filteredCandidates = {}
            candidateDictionary = model.getCandidateDictionary(sentence)
            for item in candidateDictionary:
                if (item in filter) or (item in ['^::^', '^:::^', '$:::$']):
                    filteredCandidates[item] = candidateDictionary[item]
            if len(filteredCandidates) == 0:
                randomNum = random.randrange(0, len(filter))
                return filter[randomNum]
            else:
                return self.weightedChoice(filteredCandidates)

    def generatePhrase(self, word):
        """
        Requires: models is a list of trained NGramModel objects sorted by
                  descending priority: tri-, then bi-, then unigrams.
                  desiredLength is the desired length of the phrase.
                  word is a string
        Modifies: nothing
        Effects:  returns a phrase that includes the desired word of the user
        """

        model = self.selectNGramModel([word])
        candidateDictionary = model.getCandidateDictionary([word])
        
        # Creates dictionaries for each word type
        adjDictionary = {}
        verbDictionary = {}
        nounDictionary = {}
        
        keyList = candidateDictionary.keys()
        keyString = ' '.join(keyList)

        nlp = spacy.load('en_core_web_sm')
        for token in nlp(keyString):
            if token.text in candidateDictionary:
                if token.pos_ is 'NOUN':
                    nounDictionary[token.text] = candidateDictionary[token.text]
                elif token.pos_ is 'VERB':
                    verbDictionary[token.text] = candidateDictionary[token.text]
                elif token.pos_ is 'ADJ':
                    adjDictionary[token.text] = candidateDictionary[token.text]
       
        phraseNoun = ''
        phraseVerb = ''
        phraseAdj = ''
        if self.isAdjective(word):
            phraseAdj = word
        elif self.isVerb(word):
            phraseVerb = word
        else:
            phraseNoun = word

        if phraseAdj is '' and len(adjDictionary) != 0:
            phraseAdj = self.weightedChoice(adjDictionary)
        if phraseVerb is '' and len(verbDictionary) != 0:
            phraseVerb = self.weightedChoice(verbDictionary)
        if phraseNoun is '' and len(nounDictionary) != 0:
            phraseNoun = self.weightedChoice(nounDictionary)
        
        phrase = ''
        if phraseAdj is not '':
            phrase += phraseAdj + ' '
        if phraseNoun is not '':
            phrase += phraseNoun + ' '
        if phraseVerb is not '':
            phrase += phraseVerb + ' '

        return phrase[0:len(phrase)-1].capitalize()

    def isAdjective(self, word):
        """
        Requires: word is a string
        Modifies: nothing
        Effects: returns true or false according to whether this string is an
                  an adjective or not

        """
        nlp = spacy.load('en_core_web_sm', disable=['parser','ner'])
        doc = nlp(word)
        for token in doc:
            return token.pos_ is 'ADJ'

    def isNoun(self, word):
        """
        Requires: word is a string
        Modifies: nothing
        Effects: returns true or false according to whether this string is an
                 a noun or not

        """
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        doc = nlp(word)
        for token in doc:
            return token.pos_ is 'NOUN'

    def isVerb(self, word):
        """
        Requires: word is a string
        Modifies: nothing
        Effects: returns true or false according to whether this string is an
                 a verb or not

        """
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        doc = nlp(word)
        for token in doc:
            return token.pos_ is 'VERB'


###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    model = LanguageModel()

    # Trains the data
    text = [['the', 'brown', 'fox'], ['the', 'lazy', 'dog']]
    model.updateTrainedData(text,True)

    # Testing helper methods isAdjective() and isNoun()
    print(model.isAdjective('Beautiful'))
    print(model.isAdjective('Dog'))
    print(model.isNoun('Cat'))
    print(model.isNoun('work'))
    print(model.isVerb('run'))
    print(model.isVerb('animal'))

    print(pr.rhymes('good'))

'''
    # Testing weightedChoice()
    D = {'north': 4, 'south': 1, 'east': 3, 'west': 2}
    print('Weighted choice: ' + model.weightedChoice(D))

    # Testing selectNGramModel / should print same with BiGram.py
    sentence = ["I", "love", "brown"]
    print('NGram model:', model.selectNGramModel(sentence))

    # Testing getNextToken / should print fox
    print('Next token1 is: ' + model.getNextToken(sentence, None))

    # Testing getNextToken / should print dog
    sentence = ["I", "love", "lazy"]
    print('Next token2 is: ' + model.getNextToken(sentence, None))

    # Testing getNextToken / should print brown or lazy
    sentence = ["I", "love", "the"]
    print('Next token3 is: ' + model.getNextToken(sentence, None))

    # Testing getNextToken / should print lazy
    sentence = ["I", "love", "the"]
    filter = ['lazy']
    print('Next token4 is: ' + model.getNextToken(sentence, filter))
    '''
