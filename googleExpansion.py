# -*- coding: utf-8 -*- 
import re,operator,os
import support as support
from support import sampleEvalOnFolder

def removePunctuation(text):
    r='[’!"#$%&\'()*+,.·/:;<=>?@[\\]^_`{|}~]+'
    text = re.sub(r,'',text)
    text = re.sub('  ',' ',text)
    text = re.sub('-',' ',text)
    return text

def loadStopWord():
    stopWordsDic = {}
    fp = open('I:\\bibm2016\\experiments\\english.stop')
    for line in fp.readlines():
        stopWord = line.strip()
        if stopWord not in stopWordsDic:
            stopWordsDic[stopWord] = 1
    return stopWordsDic

def isNotStopWords(word, stopWordsDic):
    if word in stopWordsDic:
        return False
    else:
        return True 

def loadMeshTerms(field):
    if field=='disease':
        meshClass = 'C'
    meshTermFile = 'I:\\Final paper\\mesh\\mtrees2015.bin'
    meshTermsDict = {}
    fp = open(meshTermFile)
    for line in fp.readlines():
        lineArr = line.strip().split(';')
        if lineArr[1][0]==meshClass:
            meshTerm = removePunctuation(lineArr[0])
            meshTermLower = ''
            meshTermList = meshTerm.strip().split(' ')
            for term in meshTermList:
                meshTermLower += term.lower()+' '
            meshTermLower = meshTermLower.strip()
            if meshTermLower not in meshTermsDict:
                meshTermsDict[meshTermLower] = 1
            
    #for meshTerm in meshTermsDict:
     #   print meshTerm       
    return meshTermsDict

def sentenceLower(sentence):
    sentenceLowerConetent = ''
    sentenceWordsList = sentence.strip().split(' ')
    for word in sentenceWordsList:
        sentenceLowerConetent += word.lower() + ' '
    sentenceLowerConetent = sentenceLowerConetent.strip()
    return sentenceLowerConetent

def collectExpansionMeshTerms(titleFile, snipFile):
    meshTermsDict = loadMeshTerms('disease')
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
                titleSentence = removePunctuation(lineArr[1])
                titleSentenceLower = sentenceLower(titleSentence)
                for meshTerm in meshTermsDict:
                    #reMesh = re.compile(meshTerm)  
                    #numberMeshTerm = len(reMesh.findall(titleSentenceLower))        
                    #if numberMeshTerm!=0:
                     #   expansionWordsCollect[queryId][meshTerm] = numberMeshTerm
                    if meshTerm not in expansionMeshWordsCollect[queryId] and titleSentenceLower.find(meshTerm)!=-1:
                        expansionMeshWordsCollect[queryId][meshTerm] = 0
                        
    for line in fpSnip.readlines():
        if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit():
                queryId = lineArr[0]
            else:
                snipSentence = removePunctuation(lineArr[1])
                snipSentenceLower = sentenceLower(snipSentence)
                for meshTerm in meshTermsDict:
                    if meshTerm not in expansionMeshWordsCollect[queryId] and snipSentenceLower.find(meshTerm)!=-1:
                        expansionMeshWordsCollect[queryId][meshTerm] = 0
    
                        
    #for queryId in expansionMeshWordsCollect:
     #   for word in expansionMeshWordsCollect[queryId]:
      #      print queryId, word, expansionMeshWordsCollect[queryId][word]   
    return expansionMeshWordsCollect

def collectExpansionWords(titleFile, snipFile):
    stopWordsDic = loadStopWord()
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
                titleSentence = removePunctuation(lineArr[1])
                titleWordsList = titleSentence.strip().split(' ')
                for word in titleWordsList:
                    wordLower = word.lower()
                    if not word.isdigit() and word!='' and isNotStopWords(wordLower, stopWordsDic):
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
                snipSentence = removePunctuation(lineArr[1])
                snipWordsList = snipSentence.strip().split(' ')
                for word in snipWordsList:
                    wordLower = word.lower()
                    if not word.isdigit() and word!='' and isNotStopWords(wordLower, stopWordsDic):
                        if wordLower not in expansionWordsCollect[queryId]:
                            expansionWordsCollect[queryId][wordLower] = 1
                        else:
                            expansionWordsCollect[queryId][wordLower] += 1
                            
    #for queryId in expansionWordsCollect:
     #   for word in expansionWordsCollect[queryId]:
      #      print queryId, word, expansionWordsCollect[queryId][word]        
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
                
    
    #for query in queryTermCount:
     #   print query, queryTermCount[query]
    queryTermInverseDoumentfreq = {}
    queryCount = len(queryTermCount)
    for term in queryTermDoumentfreq:
        queryTermDoumentfreq[term] = len(queryTermDoumentfreq[term])
        queryTermInverseDoumentfreq[term] = queryCount*1.0/queryTermDoumentfreq[term]
        #print term, queryTermDoumentfreq[term]
    
    
    #for item in sorted(queryTermInverseDoumentfreq.iteritems(), key=operator.itemgetter(1), reverse=True): 
     #   print item[0], item[1]
                
    
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
                idf = idf/len(wordList)     
                tf = tf*1.0/len(wordList)/queryTermCount[query]   
                expansionMeshWordsCollect[str(queryId)][word] = tf*idf  
            
    #for queryId in expansionMeshWordsCollect:
     #   for word in expansionMeshWordsCollect[queryId]:
      #      print queryId, word, expansionMeshWordsCollect[queryId][word] 
    return expansionMeshWordsCollect

def selectExpansionWords(expansionWordsCollect, termCountThreshold, termRankThreshold):
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

def extractOriginalWords(originalQueryFile):
    originalWords = {}
    fp = open(originalQueryFile)
    for line in fp.readlines():
        lineArr = line.strip().split(' ')
        if lineArr[0]=='<num>':
            queryId = lineArr[2]
            originalWords[queryId] = []
        if len(lineArr)>4:
            querySentence = removePunctuation(str(line.strip()))
            queryWordList = querySentence.strip().split(' ')
            for word in queryWordList:
                originalWords[queryId].append(word)
    
    #for queryId in originalWords:
     #   print queryId, originalWords[queryId]
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
    #expansionWordsCollect = collectExpansionWords('I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015Scenario\\parse_title.txt',
     #                     'I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015Scenario\\parse_snip.txt')
   
    #originalWords = extractOriginalWords('I:\\bibm2016\\experiments\\cds2015\\query\\2015OriginalQuery.txt')
    #combineExpansionOriginalWords(originalWords, expansionWordsSelect, 'no', 0.1, 'I:\\bibm2016\\experiments\\cds2015\\query\\2015GoogleScenario_7_4.query')
    
    
    
    #expansionMeshWordsCollect = collectExpansionMeshTerms('I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015Scenario\\parse_title.txt',
     #                     'I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015Scenario\\parse_snip.txt')  

    #expansionMeshWordsCollect = meshExpansionWordsAddstatisticInformation(expansionWordsCollect, expansionMeshWordsCollect)
    #expansionWordsSelect = selectExpansionWords(expansionMeshWordsCollect, 
     #                                           0.1, 
      #                                          4)
    #combineExpansionOriginalWords(originalWords, expansionWordsSelect, 'no', 0.1, 'I:\\bibm2016\\experiments\\cds2015\\query\\2015GoogleScenarioMesh_01_4.query')
    
    sampleEvalOnFolder('I:\\bibm2016\\experiments\\cds2015\\evalTool',
                       'I:\\bibm2016\\experiments\\cds2015\\qrel\\qrels-sampleval-2015.txt',
                       'I:\\bibm2016\\experiments\\cds2015\\result',
                       'I:\\bibm2016\\experiments\\cds2015\\eval')
