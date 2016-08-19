# -*- coding: utf-8 -*- 
import support
import operator, copy
import numpy as np

def collectExpansionWords(titleFile, snipFile):
    stopWordsDic = support.loadStopWord()
    fpTitle = open(titleFile)
    fpSnip = open(snipFile)
    expansionWordsCollect = {}
    for line in fpTitle.readlines():
        if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit() and lineArr[0] not in expansionWordsCollect:
                queryId = lineArr[0]
                expansionWordsCollect[queryId] = {}
                feedbackDocId = 0
            else:
                titleSentence = support.removePunctuation(lineArr[1])
                titleWordsList = titleSentence.strip().split(' ')
                for word in titleWordsList:
                    wordLower = word.lower()
                    if not word.isdigit() and word!='' and support.isNotStopWords(wordLower, stopWordsDic):
                        if wordLower not in expansionWordsCollect[queryId]:
                            expansionWordsCollect[queryId][wordLower] = {}
                            expansionWordsCollect[queryId][wordLower][feedbackDocId] = 1
                        else:
                            if feedbackDocId not in expansionWordsCollect[queryId][wordLower]:
                                expansionWordsCollect[queryId][wordLower][feedbackDocId] = 1
                            else:
                                expansionWordsCollect[queryId][wordLower][feedbackDocId] += 1
                feedbackDocId += 1
                
    for line in fpSnip.readlines():
        if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit():
                queryId = lineArr[0]
                feedbackDocId = 0
            else:
                snipSentence = support.removePunctuation(lineArr[1])
                snipWordsList = snipSentence.strip().split(' ')
                for word in snipWordsList:
                    wordLower = word.lower()
                    if not word.isdigit() and word!='' and support.isNotStopWords(wordLower, stopWordsDic):
                        if wordLower not in expansionWordsCollect[queryId]:
                            expansionWordsCollect[queryId][wordLower] = {}
                            expansionWordsCollect[queryId][wordLower][feedbackDocId] = 1
                        else:
                            if feedbackDocId not in expansionWordsCollect[queryId][wordLower]:
                                expansionWordsCollect[queryId][wordLower][feedbackDocId] = 1
                            else:
                                expansionWordsCollect[queryId][wordLower][feedbackDocId] += 1
                feedbackDocId += 1
    #support.printDict(expansionWordsCollect, 2)
                                
    return expansionWordsCollect

def meshTermDictAddSynonym(meshTermsDict, meshTermSynonymDict):
    meshTermsDictCopy = copy.deepcopy(meshTermsDict)
    for meshTerm in meshTermsDict:
        if meshTerm in meshTermSynonymDict:
            for meshTermSynonym in meshTermSynonymDict[meshTerm]:
                meshTermsDictCopy[meshTermSynonym] = 1
    #support.printDict(meshTermsDict, 2)
    return meshTermsDictCopy

def loadMeshTermsSynonym():
    meshTermSynonymDict = {}
    meshTermSynonymFile = 'I:\\bibm2016\\experiments\\mesh\\MeSHWords.txt'
    fp = open(meshTermSynonymFile)
    for line in fp.readlines():
        lineArr = line.strip().split(':')
        meshTerm = support.removePunctuation(lineArr[0])
        if meshTerm not in meshTermSynonymDict:
            meshTermSynonymDict[meshTerm] = {}
        meshTermSynonymList = lineArr[1].strip('|').split('|')
        meshTermSynonymNumber = len(meshTermSynonymList)-1
        if meshTermSynonymNumber>0:
            for meshTermSynonymIndex in range(1, meshTermSynonymNumber+1):
                meshTermSynonym = support.removePunctuation(meshTermSynonymList[meshTermSynonymIndex])
                meshTermSynonymDict[meshTerm][meshTermSynonym] = 1
                
    #support.printDict(meshTermSynonymDict, 1)
    return meshTermSynonymDict

def collectExpansionMeshTerms(titleFile, snipFile, hasSynonym):
    stopWordMeshTermDict = {'pain', 'disease'}
    meshTermsDict = support.loadMeshTerms('disease')
    if hasSynonym=='hasSynonym':
        meshTermSynonymDict = loadMeshTermsSynonym()
        meshTermsDict = meshTermDictAddSynonym(meshTermsDict, meshTermSynonymDict) 
    
    fpTitle = open(titleFile)
    fpSnip = open(snipFile)
    expansionMeshWordsCollect = {}
    for line in fpTitle.readlines():
        if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit() and lineArr[0] not in expansionMeshWordsCollect:
                queryId = lineArr[0]
                expansionMeshWordsCollect[queryId] = {}
                feedbackDocId = 0
            else:
                titleSentence = support.removePunctuation(lineArr[1])
                titleSentenceLower = support.sentenceLower(titleSentence)
                for meshTerm in meshTermsDict:
                    wordsListInTitle = titleSentenceLower.strip().split(' ')
                    meshTermLength = len(meshTerm.split(' '))
                    wordsListInTitleLength = len(wordsListInTitle)
                    titleSentenceLowerWindow = ''
                    findMeshCount = wordsListInTitleLength-meshTermLength
                    for wordIndex in range(0, findMeshCount):
                        windowSize = wordIndex+meshTermLength
                        for windowIndex in range(wordIndex, windowSize):
                            titleSentenceLowerWindow += wordsListInTitle[windowIndex]+' '
                        if titleSentenceLowerWindow.find(meshTerm)!=-1:# and meshTerm not in stopWordMeshTermDict:
                            if meshTerm not in expansionMeshWordsCollect[queryId]:
                                expansionMeshWordsCollect[queryId][meshTerm] = {}
                                expansionMeshWordsCollect[queryId][meshTerm][feedbackDocId] = 1
                            else:
                                if feedbackDocId not in expansionMeshWordsCollect[queryId][meshTerm]:
                                    expansionMeshWordsCollect[queryId][meshTerm][feedbackDocId] = 1
                                else:
                                    expansionMeshWordsCollect[queryId][meshTerm][feedbackDocId] += 1
                        titleSentenceLowerWindow = ''
                            
                feedbackDocId += 1
                        
    for line in fpSnip.readlines():
        if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit():
                queryId = lineArr[0]
                feedbackDocId = 0
            else:
                snipSentence = support.removePunctuation(lineArr[1])
                snipSentenceLower = support.sentenceLower(snipSentence)
                for meshTerm in meshTermsDict:
                    wordsListInSnip = snipSentenceLower.strip().split(' ')
                    meshTermLength = len(meshTerm.split(' '))
                    wordsListInSnipLength = len(wordsListInSnip)
                    snipSentenceLowerWindow = ''
                    meshFindCount = wordsListInSnipLength-meshTermLength
                    for wordIndex in range(0, meshFindCount):
                        windowSize = wordIndex+meshTermLength
                        for windowIndex in range(wordIndex, windowSize):
                            snipSentenceLowerWindow += wordsListInSnip[windowIndex]+' '
                        if snipSentenceLowerWindow.find(meshTerm)!=-1:# and meshTerm not in stopWordMeshTermDict:
                            if meshTerm not in expansionMeshWordsCollect[queryId]:
                                expansionMeshWordsCollect[queryId][meshTerm] = {}
                                expansionMeshWordsCollect[queryId][meshTerm][feedbackDocId] = 1
                            else:
                                if feedbackDocId not in expansionMeshWordsCollect[queryId][meshTerm]:
                                    expansionMeshWordsCollect[queryId][meshTerm][feedbackDocId] = 1
                                else:
                                    expansionMeshWordsCollect[queryId][meshTerm][feedbackDocId] += 1
                        snipSentenceLowerWindow = ''
                feedbackDocId += 1
    
    support.printDict(expansionMeshWordsCollect, 2)
    
    return expansionMeshWordsCollect

def expansionWordsTfIdf(expansionWordsCollect):
    queryTermCount = {}
    queryTermDoumentfreq = {}
    for query in expansionWordsCollect:
        queryTermCount[query] = 0
        for term in expansionWordsCollect[query]:
            queryTermCount[query] += expansionWordsCollect[query][term]
            if term not in queryTermDoumentfreq:
                queryTermDoumentfreq[term] = {}
            if query not in queryTermDoumentfreq[term]:
                queryTermDoumentfreq[term][query] = 1
    
    #print  queryTermCount[query]
              
    queryTermInverseDoumentfreq = {}
    queryCount = len(queryTermCount)
    for term in queryTermDoumentfreq:
        queryTermDoumentfreq[term] = len(queryTermDoumentfreq[term])
        queryTermInverseDoumentfreq[term] = queryCount*1.0/queryTermDoumentfreq[term]
        #print term, queryTermDoumentfreq[term]
    return queryTermCount, queryTermInverseDoumentfreq

def expansionWordsAddTfIdfInformation(expansionWordsCollect):
    queryTermCount, queryTermInverseDoumentfreq = expansionWordsTfIdf(expansionWordsCollect)
    for queryId in expansionWordsCollect:
        for word in expansionWordsCollect[queryId]:
            idf = 0.0
            tf = 0.0
            idf = queryTermInverseDoumentfreq[word]
            tf = expansionWordsCollect[queryId][word]*1.0/queryTermCount[queryId]
            expansionWordsCollect[queryId][word] = tf*idf
    
    return expansionWordsCollect

def min_mine(array):
    min_mine=100
    for item in array:
        if float(item)<min_mine:
            min_mine=float(item)
    return min_mine

def combineToOneDistributon(wordOfMeshTermList):
    wordDistributionOfOneQuery = {}
    tfList = []
   
    for feedbackDocId in range(10):
        feedbackDocIdTag = 1
        for wordDict in wordOfMeshTermList:
            if feedbackDocId not in wordDict:
                feedbackDocIdTag = 0
                
            else:
                tfList.append(wordDict[feedbackDocId])
                  
        if feedbackDocIdTag!=0:
            #print tfList
            miniTf = min_mine(tfList)
            wordDistributionOfOneQuery[feedbackDocId] = miniTf
    print  '2 ',wordOfMeshTermList       
    print wordDistributionOfOneQuery
    return wordDistributionOfOneQuery

def calculateTfIdf(expansionWordsCollect):
    tfIdfMeshWordsDict = {}
    for queryId in expansionWordsCollect:
        tfIdfMeshWordsDict[queryId] = {}
        for word in expansionWordsCollect[queryId]:
            tfIdfMeshWordsDict[queryId][word] = 0
            idf = 0.0
            tf = 0.0
            n = 0
            #idf = np.log2((10+1)*1.0/(len(expansionWordsCollect[queryId][word])+0.5))
            for queryId2 in expansionWordsCollect:
                if word in expansionWordsCollect[queryId2]:
                    n += len(expansionWordsCollect[queryId2][word])
            idf = np.log2((300+1)*1.0/(n+0.5))
            n = 0
            for feedbackDocId in expansionWordsCollect[queryId][word]:
                tf += expansionWordsCollect[queryId][word][feedbackDocId]*1.0
            tfIdfMeshWordsDict[str(queryId)][word] = tf*idf
    return tfIdfMeshWordsDict

def calculateBe(expansionWordsCollect):
    beMeshWordsDict = {}
    feedbackDocCount = 10
    Be = 0.0
    totalTf = 0.0
    tf = 0.0
    for queryId in expansionWordsCollect:
        beMeshWordsDict[queryId] = {}
        for word in expansionWordsCollect[queryId]:
            beMeshWordsDict[queryId][word] = 0.0
            for feedbackDocId in expansionWordsCollect[queryId][word]:
                totalTf += expansionWordsCollect[queryId][word][feedbackDocId]
            totalTf += 0.1
            for feedbackDocId in range(feedbackDocCount):
                if feedbackDocId in expansionWordsCollect[queryId][word]:
                    tf = expansionWordsCollect[queryId][word][feedbackDocId]
                    Be += -np.log2(feedbackDocCount - 1)-np.log2(np.e)+beFunction(feedbackDocCount+totalTf-1,feedbackDocCount+totalTf-tf-2)\
                    -beFunction(totalTf, totalTf-tf)
                else:
                    tf = 0.0
                    Be += -np.log2(feedbackDocCount - 1)-np.log2(np.e)+beFunction(feedbackDocCount+totalTf-1,feedbackDocCount+totalTf-tf-2)\
                    -beFunction(totalTf, totalTf-tf)
            beMeshWordsDict[queryId][word] = Be
            Be = 0.0
    
    return beMeshWordsDict

def beFunction(n,m):
    f = 0.0
    n = n*1.0
    m = m*1.0
    f = (m+0.5)*np.log2(n/m)+(n-m)*np.log2(n)
    return f
    

def findDiagnosis(expansionWordsDashboard):
    import re
    fp = open('I:\\trec2015\\2015bquery18.txt')
    txt = fp.read()
    queryId = 11
    diagnosisDict = {}
    for match in re.finditer(r"<diagnosis[\s\S]*?<\/diagnosis>", txt):
        diagnosisTxt = match.group()
        diagnosisTxt = diagnosisTxt.replace('<diagnosis>','').replace('</diagnosis>','')
        diagnosisTxt = support.removePunctuation(diagnosisTxt)
        diagnosisTxt = support.sentenceLower(diagnosisTxt) 
        diagnosisDict[str(queryId)] = diagnosisTxt
        queryId += 1
    
    for queryId in diagnosisDict:
        #print diagnosisDict[queryId]
        if diagnosisDict[queryId] in expansionWordsDashboard[queryId].keys():
            print queryId, diagnosisDict[queryId], expansionWordsDashboard[queryId][diagnosisDict[queryId]]
    return 0

def meshExpansionWordsAddTfIdf(expansionWordsCollect, expansionMeshWordsCollect):
    
   # queryTermCount, queryTermInverseDoumentfreq = expansionWordsTfIdf(expansionWordsCollect)
    
    tfIdfMeshWordsDict = {}            
    
    for queryId in range(1,len(expansionWordsCollect)+1):
        tfIdfMeshWordsDict[str(queryId)] = {}
        for word in expansionMeshWordsCollect[str(queryId)]:
            tfIdfMeshWordsDict[str(queryId)][word] = 0
            idf = 0.0
            tf = 0.0
            if word in expansionWordsCollect[str(queryId)]:
                idf = 10*1.0/len(expansionWordsCollect[str(queryId)][word])
                for feedbackDocId in expansionWordsCollect[str(queryId)][word]:
                    tf += expansionWordsCollect[str(queryId)][word][feedbackDocId]*1.0
                tfIdfMeshWordsDict[str(queryId)][word] = tf*idf
            else:
                wordList = word.strip().split(' ')
                wordOfMeshTermList = []
                for wordSingle in wordList:
                    if wordSingle in expansionWordsCollect[str(queryId)]:
                        print '1 ',expansionWordsCollect[str(queryId)][wordSingle]
                        wordOfMeshTermList.append(expansionWordsCollect[str(queryId)][wordSingle])
                        
                if wordOfMeshTermList == []:
                   print word
                        
                wordDistributionOfOneQuery = combineToOneDistributon(wordOfMeshTermList)
                idf = 10*1.0/len(wordDistributionOfOneQuery)
                
                for feedbackDocId in wordDistributionOfOneQuery:
                    tf += wordDistributionOfOneQuery[feedbackDocId]*1.0
                tfIdfMeshWordsDict[str(queryId)][word] = tf*idf
                 
    support.printDict(tfIdfMeshWordsDict, 2)
            
    return expansionMeshWordsCollect

def selectExpansionWordsByNormalTfIdf(expansionMeshWordsTfIdf, termCountThreshold, termRankThreshold):
    expansionWordsCollectNormal = {}
    
    for queryId in expansionMeshWordsTfIdf:
        ZNormal = 0.0
        expansionWordsCollectNormal[queryId] = {}
        for word in expansionMeshWordsTfIdf[queryId]:
            ZNormal += expansionMeshWordsTfIdf[queryId][word]
        for word in expansionMeshWordsTfIdf[queryId]:
            expansionWordsCollectNormal[queryId][word] = expansionMeshWordsTfIdf[queryId][word]*1.0/ZNormal
            
    expansionWordsSelect = {}
    expansionWordsDashboard = {}
    for queryId in expansionWordsCollectNormal:
        if queryId not in expansionWordsSelect:
            expansionWordsSelect[queryId] = {}
            expansionWordsDashboard[queryId] = {}
        count = 0
        sortExpansionTermsList = sorted(expansionWordsCollectNormal[queryId].iteritems(), key=operator.itemgetter(1), reverse=True)
        maxProb = sortExpansionTermsList[0][1]
        for item in sortExpansionTermsList: 
            #print queryId, item[0], item[1]
            itemList = item[0].split(' ')
            for itemSingle in itemList:
                if item[1] > termCountThreshold and count < termRankThreshold:
                    expansionWordsSelect[queryId][itemSingle] = item[1]/maxProb
                    count += 1
                    #NormalZ += item[1]
                    print queryId, item[0], item[1], count
                    if item[0] not in expansionWordsDashboard[queryId]:
                        expansionWordsDashboard[queryId][item[0]] = [item[1], count]
        #for expansionTerm in expansionWordsSelect[queryId]:
            #expansionWordsSelect[queryId][expansionTerm] = expansionWordsSelect[queryId][expansionTerm]/NormalZ
    expansionWordsNumber = 0
    for queryId in expansionWordsSelect:
        #print queryId, expansionWordsSelect[queryId]
        expansionWordsNumber += len(expansionWordsSelect[queryId])
    print termRankThreshold, expansionWordsNumber*1.0/30
    
    #support.printDict(expansionWordsDashboard, 2)
    return expansionWordsSelect, expansionWordsDashboard

def combineExpansionOriginalWordsWeightDifferent(originalWords, expansionWordsSelect, weightExpansionWords, combineQueryFile):
    queryExpansionContent = ''
    for queryId in range(1,len(originalWords)+1):
        queryExpansionContent += '<top>\n\n'+'<num> Number: '+str(queryId)+'\n\n'+'<desc>\n\n'
        lengthOrigialWords = len(originalWords[str(queryId)])
        #lengthExpansionWords = len(expansionWordsSelect[str(queryId)])
        for originalWordIndex in range(lengthOrigialWords):  
            queryExpansionContent += originalWords[str(queryId)][originalWordIndex]+'^'+str(1-weightExpansionWords)+' '#+'\n\n'+r'</top>'+'\n\n'
        for expansionWord in expansionWordsSelect[str(queryId)]:
            queryExpansionContent += expansionWord+'^'+str(weightExpansionWords*expansionWordsSelect[str(queryId)][expansionWord])+' '
        queryExpansionContent += '\n\n'+r'</top>'+'\n\n'
    support.saveFile(queryExpansionContent.replace('xray', 'x-ray'), combineQueryFile)
    return 0

def adjustWeight(lowIndex, highIndex, unit, originalWords, expansionWordsSelect):
    for expansionWordsWeight in range(lowIndex, highIndex+1, unit):
        combineExpansionOriginalWordsWeightDifferent(originalWords, 
                                                expansionWordsSelect, 
                                                expansionWordsWeight*1.0/10, 
                                                'I:\\bibm2016\\experiments\\cds2014\\query\\differentWeightAmongExpansionWords\\2014HowToScenarioGoogleMeshNormal_01_3_0'+str(expansionWordsWeight)+'.query')
    return 0

def adjustExpansionWordsNumber(expansionMeshWordsCollect, originalWords):
    for expansionWordsNumber in range(1,10):
        expansionWordsSelect = selectExpansionWordsByNormalTfIdf(expansionMeshWordsCollect, 
                                                0.1, 
                                                expansionWordsNumber)
        combineExpansionOriginalWordsWeightDifferent(originalWords, 
                                                expansionWordsSelect, 
                                                0.5, 
                                                'I:\\bibm2016\\experiments\\cds2014\\query\\expansionWordsNumber\\2014HowToScenarioGoogleMeshNormal_01_'+str(expansionWordsNumber)+'_05.query')
    return 0

if __name__ == "__main__":  
    #expansionWordsCollect = collectExpansionWords('I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015HowToScenario\\parse_title.txt',
     #                     'I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015HowToScenario\\parse_snip.txt')

    originalWords = support.extractOriginalWords('I:\\bibm2016\\experiments\\cds2015\\query\\2015OriginalQuery.txt')
    
    #expansionMeshWordsCollect = collectExpansionMeshTerms('I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015HowToScenario\\parse_title.txt',
     #                     'I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015HowToScenario\\parse_snip.txt',
      #                    'hasSynonym')  
       #                     #'noSynonym')
    #support.storeweakClassArr(expansionMeshWordsCollect, 
     #                         'H:\\Users2016\\hy\\workspace\\bibm2016\\collectExpansionWords\\expansionMeshWordsCollect.txt')
     
    expansionMeshWordsCollect = support.grabweakClassArr('H:\\Users2016\\hy\\workspace\\bibm2016\\collectExpansionWords\\expansionMeshWordsCollect.txt') 
    
    expansionMeshWordsTfIdf = calculateTfIdf(expansionMeshWordsCollect) 
    
    #expansionMeshWordsBe= calculateBe(expansionWordsCollect) 
    
    #support.printDict(expansionMeshWordsBe, 2)
    
    #expansionMeshWordsCollect = meshExpansionWordsAddTfIdf(expansionWordsCollect, expansionMeshWordsCollect)
    ##expansionWordsCollect = expansionWordsAddTfIdfInformation(expansionWordsCollect)
    
    expansionWordsSelect, expansionWordsDashboard = selectExpansionWordsByNormalTfIdf(expansionMeshWordsTfIdf, 
                                                                                      0.05, 
                                                                                      3)
    
    findDiagnosis(expansionWordsDashboard)
    
    combineExpansionOriginalWordsWeightDifferent(originalWords, 
                                                expansionWordsSelect, 
                                                0.5,    
                                                'I:\\bibm2016\\experiments\\cds2015\\query\\final3\\2015HowToScenarioGoogleTfIdfMeshSynonymNormal_005_3_05.query')
    #adjustWeight(1,9,1, originalWords, expansionWordsSelect)
    #adjustExpansionWordsNumber(expansionMeshWordsCollect)
    