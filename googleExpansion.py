# -*- coding: utf-8 -*- 
import re,operator,os,copy
import support as support
import numpy as np
from support import sampleEvalOnFolder

def meshTermDictAddSynonym(meshTermsDict, meshTermSynonymDict):
    meshTermsDictCopy = copy.deepcopy(meshTermsDict)
    for meshTerm in meshTermsDict:
        if meshTerm in meshTermSynonymDict:
            for meshTermSynonym in meshTermSynonymDict[meshTerm]:
                meshTermsDictCopy[meshTermSynonym] = 1
    #support.printDict(meshTermsDict, 2)
    return meshTermsDictCopy

def collectExpansionMeshTerms(titleFile, snipFile):
    stopWordMeshTermDict = {'pain', 'disease'}
    meshTermsDict = support.loadMeshTerms('disease')
    #meshTermSynonymDict = loadMeshTermsSynonym()
    #meshTermsDict = meshTermDictAddSynonym(meshTermsDict, meshTermSynonymDict) 
    
    fpTitle = open(titleFile)
    fpSnip = open(snipFile)
    expansionMeshWordsCollect = {}
    for line in fpTitle.readlines():
        if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit() and lineArr[0] not in expansionMeshWordsCollect:
                queryId = lineArr[0]
                expansionMeshWordsCollect[queryId] = {}
            else:
                titleSentence = support.removePunctuation(lineArr[1])
                titleSentenceLower = support.sentenceLower(titleSentence)
                for meshTerm in meshTermsDict:
                    #reMesh = re.compile(meshTerm)  
                    #numberMeshTerm = len(reMesh.findall(titleSentenceLower))        
                    #if numberMeshTerm!=0:
                     #   expansionWordsCollect[queryId][meshTerm] = numberMeshTerm
                    if meshTerm not in expansionMeshWordsCollect[queryId] and titleSentenceLower.find(meshTerm)!=-1 and meshTerm not in stopWordMeshTermDict:
                        expansionMeshWordsCollect[queryId][meshTerm] = 0
                        
    for line in fpSnip.readlines():
        if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit():
                queryId = lineArr[0]
            else:
                snipSentence = support.removePunctuation(lineArr[1])
                snipSentenceLower = support.sentenceLower(snipSentence)
                for meshTerm in meshTermsDict:
                    if meshTerm not in expansionMeshWordsCollect[queryId] and snipSentenceLower.find(meshTerm)!=-1 and meshTerm not in stopWordMeshTermDict:
                        expansionMeshWordsCollect[queryId][meshTerm] = 0
    
    return expansionMeshWordsCollect

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
            else:
                titleSentence = support.removePunctuation(lineArr[1])
                titleWordsList = titleSentence.strip().split(' ')
                for word in titleWordsList:
                    wordLower = word.lower()
                    if not word.isdigit() and word!='' and support.isNotStopWords(wordLower, stopWordsDic):
                        if wordLower not in expansionWordsCollect[queryId]:
                            expansionWordsCollect[queryId][wordLower] = 1
                        else:
                            expansionWordsCollect[queryId][wordLower] += 1
                
    for line in fpSnip.readlines():
        if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit():
                queryId = lineArr[0]
            else:
                snipSentence = support.removePunctuation(lineArr[1])
                snipWordsList = snipSentence.strip().split(' ')
                for word in snipWordsList:
                    wordLower = word.lower()
                    if not word.isdigit() and word!='' and support.isNotStopWords(wordLower, stopWordsDic):
                        if wordLower not in expansionWordsCollect[queryId]:
                            expansionWordsCollect[queryId][wordLower] = 1
                        else:
                            expansionWordsCollect[queryId][wordLower] += 1
                                
    return expansionWordsCollect

def meshExpansionWordsAddstatisticInformation(expansionWordsCollect, expansionMeshWordsCollect):
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
                
    queryTermInverseDoumentfreq = {}
    queryCount = len(queryTermCount)
    for term in queryTermDoumentfreq:
        queryTermDoumentfreq[term] = len(queryTermDoumentfreq[term])
        queryTermInverseDoumentfreq[term] = queryCount*1.0/queryTermDoumentfreq[term]
        #print term, queryTermDoumentfreq[term]
                
    
    for queryId in range(1,len(expansionWordsCollect)+1):
        for word in expansionMeshWordsCollect[str(queryId)]:
            idf = 0.0
            tf = 0.0
            if word in expansionWordsCollect[str(queryId)]:
                idf = queryTermInverseDoumentfreq[word]
                tf = expansionWordsCollect[str(queryId)][word]*1.0/queryTermCount[query]
                expansionMeshWordsCollect[str(queryId)][word] = tf*idf
            else:
                wordList = word.strip().split(' ')
                for wordSingle in wordList:
                    if wordSingle in expansionWordsCollect[str(queryId)]:
                        tf += expansionWordsCollect[str(queryId)][wordSingle]
                        idf += queryTermInverseDoumentfreq[wordSingle]
                    else:
                        tf = 1.0
                        idf = 0.1
                idf = idf/len(wordList)     
                tf = tf*1.0/len(wordList)/queryTermCount[query]   
                expansionMeshWordsCollect[str(queryId)][word] = tf*idf  
            
    return expansionMeshWordsCollect

def selectExpansionWordsByTfIdf(expansionWordsCollect, termCountThreshold, termRankThreshold):
    expansionWordsSelect = {}
    for queryId in expansionWordsCollect:
        if queryId not in expansionWordsSelect:
            expansionWordsSelect[queryId] = []
        count = 0
        for item in sorted(expansionWordsCollect[queryId].iteritems(), key=operator.itemgetter(1), reverse=True): 
            print queryId, item[0], item[1]
            itemList = item[0].split(' ')
            for itemSingle in itemList:
                if item[1] > termCountThreshold and count < termRankThreshold:
                    expansionWordsSelect[queryId].append(itemSingle)
                    count += 1
    for queryId in expansionWordsSelect:
        print queryId, expansionWordsSelect[queryId]
    return expansionWordsSelect

def selectExpansionWordsByNormalTfIdf(expansionWordsCollect, termCountThreshold, termRankThreshold):
    expansionWordsCollectNormal = {}
    
    for queryId in expansionWordsCollect:
        ZNormal = 0.0
        expansionWordsCollectNormal[queryId] = {}
        for word in expansionWordsCollect[queryId]:
            ZNormal += expansionWordsCollect[queryId][word]
        for word in expansionWordsCollect[queryId]:
            expansionWordsCollectNormal[queryId][word] = expansionWordsCollect[queryId][word]*1.0/ZNormal
            
    expansionWordsSelect = {}
    for queryId in expansionWordsCollectNormal:
        if queryId not in expansionWordsSelect:
            expansionWordsSelect[queryId] = []
        count = 0
        for item in sorted(expansionWordsCollectNormal[queryId].iteritems(), key=operator.itemgetter(1), reverse=True): 
            #print queryId, item[0], item[1]
            itemList = item[0].split(' ')
            for itemSingle in itemList:
                if item[1] > termCountThreshold and count < termRankThreshold:
                    expansionWordsSelect[queryId].append(itemSingle)
                    count += 1
                    print queryId, item[0], item[1]
    for queryId in expansionWordsSelect:
        print queryId, expansionWordsSelect[queryId]
    return expansionWordsSelect

def extractOriginalWords(originalQueryFile):
    originalWords = {}
    fp = open(originalQueryFile)
    for line in fp.readlines():
        lineArr = line.strip().split(' ')
        if lineArr[0]=='<num>':
            queryId = lineArr[2]
            originalWords[queryId] = []
        if len(lineArr)>4:
            querySentence = support.removePunctuation(str(line.strip()))
            queryWordList = querySentence.strip().split(' ')
            for word in queryWordList:
                originalWords[queryId].append(word)
    
    return originalWords

def combineExpansionOriginalWords(originalWords, expansionWordsSelect, hasWeight, weightOriginalWords, combineQueryFile):
    queryExpansionContent = ''
    if hasWeight=='no':
        for queryId in range(1,len(originalWords)+1):
            queryExpansionContent += '<top>\n\n'+'<num> Number: '+str(queryId)+'\n\n'+'<desc>\n\n'
            for originalWordIndex in range(len(originalWords[str(queryId)])):  
                queryExpansionContent += originalWords[str(queryId)][originalWordIndex]+' '#+'\n\n'+r'</top>'+'\n\n'
            for expansionWordIndex in range(len(expansionWordsSelect[str(queryId)])):
                queryExpansionContent += expansionWordsSelect[str(queryId)][expansionWordIndex] + ' '
            queryExpansionContent += '\n\n'+r'</top>'+'\n\n'
        #print queryExpansionContent
    support.saveFile(queryExpansionContent.replace('xray', 'x-ray'), combineQueryFile)
    return 0

if __name__ == "__main__":  
    expansionWordsCollect = collectExpansionWords('I:\\bibm2016\\experiments\\GoogleSearch\\result\\Scenario2015\\parse_title.txt',
                          'I:\\bibm2016\\experiments\\GoogleSearch\\result\\Scenario2015\\parse_snip.txt')

    originalWords = extractOriginalWords('I:\\bibm2016\\experiments\\cds2015\\query\\2015OriginalQuery.txt')
    
    
    
    
    expansionMeshWordsCollect = collectExpansionMeshTerms('I:\\bibm2016\\experiments\\GoogleSearch\\result\\Scenario2015\\parse_title.txt',
                          'I:\\bibm2016\\experiments\\GoogleSearch\\result\\Scenario2015\\parse_snip.txt')  

    expansionMeshWordsCollect = meshExpansionWordsAddstatisticInformation(expansionWordsCollect, expansionMeshWordsCollect)
    expansionWordsSelect = selectExpansionWordsByNormalTfIdf(expansionMeshWordsCollect, 
                                                0.1, 
                                                3)
    #combineExpansionOriginalWords(originalWords, expansionWordsSelect, 'no', 0.1, 'I:\\bibm2016\\experiments\\cds2015\\query\\2015GoogleOriginalMeshNormal_01_4.query')
    combineExpansionOriginalWords(originalWords, expansionWordsSelect, 'no', 0.1, 'I:\\bibm2016\\experiments\\cds2015\\query\\2015ScenarioGoogleMeshNormal_01_3.query')
    
    
    