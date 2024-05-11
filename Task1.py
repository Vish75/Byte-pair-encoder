import collections


# Helper functions

def vocabularyCreation(wordFrequency):
    charList = set()
    for i in wordFrequency:
        wordList = i.split('-')
        for k in wordList:
            charList.add(k)
    return charList

def pairFrequencis(wordFrequency):
    pair = collections.defaultdict(int)
    for word, wordFreq in wordFrequency.items():
        charList = word.split('-')
        if len(charList)==1:
            continue
        for i in range(len(charList)-1):
            pair[charList[i],charList[i+1]] += wordFreq
    return pair

def findBestPair(characterPairs):
    return max(characterPairs, key=characterPairs.get)

def removeMergedPair(characterPairs, bestPair):
    newCharacterPairs = characterPairs.pop(bestPair)
    return newCharacterPairs

def mergePairs(pair, vocabulary, mergeRules, wordFreq):
    newWordFreq = {}
    charOne, charTwo = pair
    if(charOne in vocabulary and charTwo in vocabulary):
        vocabulary.add(''.join(pair))
    mergeRules.append((charOne, charTwo))
    for word in wordFreq:
        wordList = word.split('-')
        if charOne in wordList and charTwo in wordList:
            indicesCharOne = [i for i in range(len(wordList)) if wordList[i] == charOne]
            indicesCharTwo = [i for i in range(len(wordList)) if wordList[i] == charTwo]
            for i in indicesCharOne:
                for j in indicesCharTwo:
                    
                    if (i - j)==-1:
                        wordList[i] = ''.join(pair)
                        wordList[j] = '-'
        while '-' in wordList:
            wordList.remove('-')
        newWord = ""
        for j in wordList:
            newWord+=j
            if(j!=wordList[-1]):
                newWord += '-'
        newWordFreq[newWord] = wordFreq[word]
    return vocabulary, mergeRules, newWordFreq

def corpusCreation():
    workingCorpus = []
    with open('corpus.txt','r') as file:
        corpus = file.readlines()
    for i in corpus:
        i=i[:-1]
        workingCorpus.append(i)
    return workingCorpus

def wordFrequency(corpus):
    wordFrequency = {}
    for i in corpus:
        sentenceSplit = i.split()
        for j in sentenceSplit:
            newWord = ""
            for k in range(len(j)):
                newWord+=j[k]+"-"
            newWord += '$'
            if newWord in wordFrequency.keys():
                wordFrequency[newWord]+=1
            else:
                wordFrequency[newWord] = 1
    return wordFrequency

def wordToChar(word):
    charList = []
    for i in word:
        if i!='-':
            charList.append(i)
    return charList
    
# Class

class Tokenizer:
    
    
    # Helper variables
    mergeRules = []
    corpus = corpusCreation()
    wordFreq = wordFrequency(corpus)


    
    # Defined methods
    def learn_vocabulary(self, numberOfMerges):
        for i in range(numberOfMerges):
            vocabulary = vocabularyCreation(self.wordFreq)
            characterPairs = pairFrequencis(self.wordFreq)
            bestPair = findBestPair(characterPairs)
            characterPairs = removeMergedPair(characterPairs, bestPair)
            vocabulary, self.mergeRules, self.wordFreq = mergePairs(bestPair, vocabulary, self.mergeRules, self.wordFreq)
        return vocabulary, self.mergeRules
    
    def tokenizeSample(self):
        wordInitial = input("Enter the sample: ")
        wordList = wordInitial.split()
        wordOutput = []
        for wordInput in wordList:

            wordInput += '$'
            wordInChar = wordToChar(wordInput)
            
            for k in self.mergeRules:
                charOne, charTwo = k
                if charOne in wordInChar and charTwo in wordInChar:
                    indicesCharOne = [i for i in range(len(wordInChar)) if wordInChar[i] == charOne]
                    indicesCharTwo = [i for i in range(len(wordInChar)) if wordInChar[i] == charTwo]
                    for i in indicesCharOne:
                        for j in indicesCharTwo:
                            if (i - j)==-1:
                                wordInChar[i] = ''.join(k)
                                wordInChar.pop(j)
            wordText = ""     
            for j in range(len(wordInChar)-1):
                wordText+=wordInChar[j]+"-"
            wordText+=wordInChar[-1]
            wordOutput.append(wordText)
        return wordOutput

"""
mergeRules = []
corpus = corpusCreation()
wordFreq = wordFrequency(corpus)

# for loop for number of merges
numberOfMerges = 5
for i in range(numberOfMerges):
    print("Merge no. {}".format(i+1))
    vocabulary = vocabularyCreation(wordFreq)
    print("\nThe initial vocabulary is: {}".format(vocabulary))
    characterPairs = pairFrequencis(wordFreq)
    print("\nThe character pairs are: {}".format(characterPairs))
    bestPair = max(characterPairs, key=characterPairs.get)
    print("\nThe best pair is: {}".format(bestPair))
    characterPairs.pop(bestPair)
    vocabulary, mergeRules, wordFreq = mergePairs(bestPair, vocabulary, mergeRules, wordFreq)
    print("\nThe new vocabulary is: {}".format(vocabulary))
    print("\nThe merge rules are: {}".format(mergeRules))
    print("\nThe word have changed to: {}\n\n".format(wordFreq))


wordInput = input("Enter a word: ")
wordInput += '$'
wordInChar = wordToChar(wordInput)
print(wordInChar)
tokenizedWord = tokenizeSample(wordInChar, mergeRules)
print(tokenizedWord)
"""
# Learning vocabulary and merge rules:
numberOfMerges = int(input("Enter the number of merges: "))
tokenizationClass = Tokenizer()
vocabulary, mergeRules = tokenizationClass.learn_vocabulary(numberOfMerges)

# Tokenizing words
numOfWords = int(input("How many samples of words you need to enter: "))
tokenizedWords = []
for i in range(numOfWords):
    outputWord = tokenizationClass.tokenizeSample()
    tokenizedWords.append(outputWord)

# File handling

# Vocabulary
with open('tokens.txt','w') as file:
    for vocabularyWord in vocabulary:
        file.write("%s\n"%vocabularyWord)
file.close()

# Merge rules
with open('merge_rules.txt','w') as file:
    for mergeRule in mergeRules:
        file.write("%s -> %s\n"%(mergeRule,''.join(mergeRule)))
file.close()

# Tokenized samples
with open('tokenized_samples.txt','w') as file:
    for word in tokenizedWords:
        newWord = ""
        for instances in word:
            newWord+=instances+" "
        file.write("%s\n"%newWord)
file.close()
