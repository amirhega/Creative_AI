from creative_ai.utils.print_helpers import ppGramJson

class TrigramModel():

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
        Modifies: self.nGramCounts, a three-dimensional dictionary. 
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries as values,
                  where those inner dictionaries have strings as keys
                  and dictionaries of {string: integer} pairs as values.
        """
        for sentence in text:
          for i in range(0, len(sentence) - 2):
            if sentence[i] not in self.nGramCounts:
              self.nGramCounts[sentence[i]] = {}

            if sentence[i + 1] not in self.nGramCounts[sentence[i]]:
              self.nGramCounts[sentence[i]][sentence[i + 1]] = {}

            if sentence[i + 2] not in self.nGramCounts[sentence[i]][sentence[i+1]]:
              self.nGramCounts[sentence[i]][sentence[i + 1]][sentence[i+2]] = 0

            self.nGramCounts[sentence[i]][sentence[i+1]][sentence[i+2]] += 1



    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. 
        """
        return len(sentence) >= 2 and sentence[-2] in self.nGramCounts and sentence[-1] in self.nGramCounts[sentence[-2]]

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. 
        """
        return self.nGramCounts[sentence[-2]][sentence[-1]]

###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # An example trainModel test case
    uni = TrigramModel()

    text = [ ['the', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    uni.trainModel(text)
    #{"'the'": {"'brown'": {"'fox'": 1}, "'lazy'": {"'dog'": 1 }}}
    print(uni)
    
    text0 = ['the', 'brown']
    #should print true
    print(uni.trainingDataHasNGram(text0))
    
    text1 = ['the', 'brown', 'dog', 'the', 'lazy']
    #should print true
    print(uni.trainingDataHasNGram(text1))

    text1 = ['the', 'brown', 'dog']
    #should print false
    print(uni.trainingDataHasNGram(text1))

    sentence = ['i', 'the', 'brown']

    print(uni.getCandidateDictionary(sentence)) #should return {'fox': 1}