import support

def meshExpansion(originalWords):
    meshExpansionWordsDict = {}
    meshTermSynonymDict = support.loadMeshTermsSynonym()
    for queryId in originalWords:
        meshExpansionWordsDict[queryId] = []
        querySecntence = ''
        for word in originalWords[queryId]:
            querySecntence += word + ' '
        for meshTerm in meshTermSynonymDict:
            for meshTermSynonymWord in meshTermSynonymDict[meshTerm]:
                if querySecntence.find(meshTermSynonymWord)!=-1:
                    meshExpansionWordsDict[queryId].append(list(meshTermSynonymDict[meshTerm])[0])
                    break
    support.printDict(meshExpansionWordsDict, 1)
    return meshExpansionWordsDict

def combineExpansionOriginalWordsWeightSame(originalWords, expansionWordsSelect, hasWeight, weightExpansionWords, combineQueryFile):
    queryExpansionContent = ''
    if hasWeight=='no':
        for queryId in range(1,len(originalWords)+1):
            queryExpansionContent += '<top>\n\n'+'<num> Number: '+str(queryId)+'\n\n'+'<desc>\n\n'
            lengthOrigialWords = len(originalWords[str(queryId)])
            lengthExpansionWords = len(expansionWordsSelect[str(queryId)])
            for originalWordIndex in range(lengthOrigialWords):  
                queryExpansionContent += originalWords[str(queryId)][originalWordIndex]+' '#+'\n\n'+r'</top>'+'\n\n'
            for expansionWordIndex in range(lengthExpansionWords):
                queryExpansionContent += expansionWordsSelect[str(queryId)][expansionWordIndex] + ' '
            queryExpansionContent += '\n\n'+r'</top>'+'\n\n'
        #print queryExpansionContent
    elif hasWeight=='yes':
        for queryId in range(1,len(originalWords)+1):
            queryExpansionContent += '<top>\n\n'+'<num> Number: '+str(queryId)+'\n\n'+'<desc>\n\n'
            lengthOrigialWords = len(originalWords[str(queryId)])
            lengthExpansionWords = len(expansionWordsSelect[str(queryId)])
            for originalWordIndex in range(lengthOrigialWords):  
                queryExpansionContent += originalWords[str(queryId)][originalWordIndex]+'^'+str(1-weightExpansionWords)+' '#+'\n\n'+r'</top>'+'\n\n'
            for expansionWordIndex in range(lengthExpansionWords):
                queryExpansionContent += expansionWordsSelect[str(queryId)][expansionWordIndex]+'^'+str(weightExpansionWords)+' '
            queryExpansionContent += '\n\n'+r'</top>'+'\n\n'
    support.saveFile(queryExpansionContent.replace('xray', 'x-ray'), combineQueryFile)
    return 0

if __name__ == "__main__":  
    originalWords = support.extractOriginalWords('I:\\bibm2016\\experiments\\cds2014\\query\\2014OriginalQuery.txt')
    meshExpansionWordsDict = meshExpansion(originalWords)
    combineExpansionOriginalWordsWeightSame(originalWords, meshExpansionWordsDict, 'yes', 0.2, 'I:\\bibm2016\\experiments\\cds2014\\query\\final\\2014MeshExpansion_02.query')
    
   