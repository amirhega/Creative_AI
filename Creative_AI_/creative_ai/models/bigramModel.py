from creative_ai.utils.print_helpers import ppGramJson

class BigramModel():

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  This is the NGramModel constructor. It sets up an empty
                  dictionary as a member variable.
        
        """
        self.nGramCounts = {}

    def __str__(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  Returns the string to print when you call print on an
                  NGramModel object. This string will be formatted in JSON
                  and display the currently trained dataset.
        
        """

        return ppGramJson(self.nGramCounts)


###############################################################################
# >> CORE IMPLEMENTION <<
###############################################################################

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a two-dimensional dictionary. 
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries of
                  {string: integer} pairs as values.
        """
        for sentence in text:
          for i in range(0, len(sentence) - 1):
            if sentence[i] not in self.nGramCounts:
              self.nGramCounts[sentence[i]] = {}

            if sentence[i + 1] not in self.nGramCounts[sentence[i]]:
              self.nGramCounts[sentence[i]][sentence[i + 1]] = 0

            self.nGramCounts[sentence[i]][sentence[i + 1]] += 1


    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. 
        """
        return sentence[-1] in self.nGramCounts

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. 
        """
        return self.nGramCounts[sentence[-1]]

###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':

    # An example trainModel test case
    bi = BigramModel()
    text = [ [ 'brown' ] ]
    bi.trainModel(text)
    # Should print: {}
    print(bi)

    text = [ ['the', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    bi.trainModel(text)
    # Should print: { 'brown': {'fox': 1}, 'lazy': {'dog': 1}, 'the': {'brown': 1, 'lazy': 1} }
    print(bi)

    # An example trainingDataHasNGram test case
    bi = BigramModel()
    sentence = ["I", "love", "the"]
    print(bi.trainingDataHasNGram(sentence)) # should be False
    bi.trainModel(text)
    print(bi.trainingDataHasNGram(sentence)) # should be True

    print(bi.getCandidateDictionary(sentence)) # should be {'brown': 1, 'lazy': 1}

