# Creative AI Twitter Bot

-Amar Ramachandan
-Amir Hegazy
-Liam Clancy
-Sinan Karabocuoglu

Python Libraries Used:
*tweepy
*pysynth
*pronouncing
*spacy
*random

The application of our project is to create unique 6-line country verse for our users by a Twitter Bot. Our verses are based on a single word that our users provide to our bot via their Twitter Accounts.

For the heuristics part of our project we focused on creating a phrase--will be used at the beginning of the first and last lines of our song--based on our users' word with the spacy library. Moreover, we also used the pronouncing library to find possible rhyming words at the end of our lines, and passed these rhyming words through the filter of generateTokenSentence function in order to create rhymes between the 2nd and 4th lines and 3rd and 5th lines.

Finally, for the Showmanship component of our project we created a Twitter Bot called @CountryBot1, which can be used to submit desired words to our AI applicaiton. Then our bot will reply to the user tweet with the unique 6-line country verse. To do so, we used the tweepy library of Python.
