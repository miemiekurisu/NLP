from numpy import * 
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', \
                          'problems', 'help', 'please'],
                         ['maybe', 'not', 'take', 'him', \
                          'to', 'dog', 'park', 'stupid'],
                         ['my', 'dalmation', 'is', 'so', 'cute', \
                           'I', 'love', 'him'],
                         ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                         ['mr', 'licks', 'ate', 'my', 'steak', 'how',\
                           'to', 'stop', 'him'],
                         ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1] #1 is abusive, 0 not
    return postingList,classVec
    
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)
    
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1 #Create a vector D of all 0s
        else: print "the word: %s is not in my Vocabulary!" % word
    return returnVec
    
def prepareMatrix():
    postingList,classVec = loadDataSet()
    retMatrix = []
    vocabList = createVocabList(postingList)
    for l in postingList:
        retMatrix.append(setOfWords2Vec(vocabList,l))
    return retMatrix,classVec
    
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            #print "p1Num=%r"%p1Num
            p1Denom += sum(trainMatrix[i])
            #print "p1Denom=%r"%p1Denom
        else:
            p0Num += trainMatrix[i]
            #print "p0Num=%r"%p0Num
            p0Denom += sum(trainMatrix[i])
            #print "p0Denom=%r"%p0Denom
    p1Vect = log(p1Num/p1Denom)
    #print p1Num
    p0Vect = log(p0Num/p0Denom)
    #print p0Num
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0-pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def bagOfWords2vecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        returnVec[vocabList.index(word)]+=1
    return returnVec

def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat=[]
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
    p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses))
    testEntry = ['love','my','dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList,testEntry))
    print testEntry,'classified as:',classifyNB(thisDoc,p0V,p1V,pAb)
    testEntry = ['stupid','garbage']
    thisDoc = array(setOfWords2Vec(myVocabList,testEntry))
    print testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb)

def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W*',bigString)
    tk = []
    for tok in listOfTokens:
        if len(tok) >1 and re.findall('\D+',tok)!=[] :
            tk.append(tok.lower())
    return tk

def spamTest():
    docList = []
    classList = []
    fullText = []
    for i in range(1,26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50)
    testSet=[]
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    #print 'the error rate is: ',float(errorCount)/len(testSet)
    return float(errorCount)/len(testSet)
    
def calcMostFreq(vocabList,fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token]=fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedFreq[:30]
    
def localWords(feed1,feed0):
    import feedparser
    docList=[];classList=[];fullText=[]
    