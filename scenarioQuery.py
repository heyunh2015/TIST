import support

def interSetResult(resultFileA, resultFileB):
    fpA = open(resultFileA)
    fpB = open(resultFileB)
    resultDictA = {}
    resultDictB = {}
    for line in fpA.readlines():
         if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit() and lineArr[0] not in resultDictA:
                queryId = lineArr[0]
                resultDictA[queryId] = []
            else:
                resultDictA[queryId].append(lineArr[1])
    
    for line in fpB.readlines():
         if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit() and lineArr[0] not in resultDictB:
                queryId = lineArr[0]
                resultDictB[queryId] = []
            else:
                resultDictB[queryId].append(lineArr[1])
    
    statisticDict = {}
    
    interSetDiagnosis = 0
    interSetTest = 0
    interSetTreatment = 0
    for queryId in range(1,len(resultDictA)+1):
        interSetNumber = len(set(resultDictA[str(queryId)])&set(resultDictB[str(queryId)]))
        if queryId>0 and queryId<11:
            interSetDiagnosis += interSetNumber
        elif queryId>=11 and queryId<21:
            interSetTest += interSetNumber
        elif queryId>=21 and queryId<=30:
            interSetTreatment += interSetNumber
        print queryId, interSetNumber
        if interSetNumber not in statisticDict:
            statisticDict[interSetNumber] = 1
        else:
            statisticDict[interSetNumber] += 1
    
    support.printDict(statisticDict, 1)
    print 'interSetDiagnosis ', interSetDiagnosis
    print 'interSetTest ', interSetTest
    print 'interSetTreatment ', interSetTreatment
    return 0

def addScenarioWord(originalQueryFile, scenarioWordsList, scenarioQueryFile):
    scenarioQuery = ''
    fp = open(originalQueryFile)
    for line in fp.readlines():
        lineArr = line.strip().split('\t')
        if int(lineArr[0])>0 and int(lineArr[0])<11:
            scenarioQuery += lineArr[0]+'\t'+lineArr[1]+' '+scenarioWordsList[0]+'\n'
        elif int(lineArr[0])>10 and int(lineArr[0])<21:
            scenarioQuery += lineArr[0]+'\t'+lineArr[1]+' '+scenarioWordsList[1]+'\n'
        elif int(lineArr[0])>20 and int(lineArr[0])<31:
            scenarioQuery += lineArr[0]+'\t'+lineArr[1]+' '+scenarioWordsList[2]+'\n'
    support.saveFile(scenarioQuery, scenarioQueryFile)
    return 0

if __name__ == "__main__":  
    #interSetResult('I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015Original\\parse_title.txt',
     #              'I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015Scenario\\parse_title.txt')
     addScenarioWord('I:\\bibm2016\\experiments\\GoogleSearch\\data\\2016.CDSid_queryOriginal.txt',
                     ['how to diagnosis','how to test','how to treatment'],
                     'I:\\bibm2016\\experiments\\GoogleSearch\\data\\2016.CDSid_queryHowToScenario.txt')
    
    