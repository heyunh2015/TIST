import support

def extractMeshSynonymDisease():
    meshClass = 'C'
    meshTermFile = 'I:\\bibm2016\\experiments\\mesh\\mtrees2015.bin'
    meshTermsDict = {}
    fp = open(meshTermFile)
    for line in fp.readlines():
        lineArr = line.strip().split(';')
        if lineArr[1][0]==meshClass:
            meshTermLower = lineArr[0].lower()
            meshTermsDict[meshTermLower] = 1
            
    #support.printDict(meshTermsDict, 1)
    meshSynonymFile = 'I:\\bibm2016\\experiments\\mesh\\MeSHWords.txt'
    meshSynonymDiseaseFile = 'I:\\bibm2016\\experiments\\mesh\\MeSHWords_disease.txt'
    meshSynonymDiseaseTxt = ''
    fpSynonym = open(meshSynonymFile)
    for line in fpSynonym.readlines():
        lineArr = line.strip().split(':');
        if lineArr[0] in meshTermsDict:
            meshSynonymDiseaseTxt += str(line)
    
    fpSysnonymDisease = open(meshSynonymDiseaseFile, 'w')
    fpSysnonymDisease.write(meshSynonymDiseaseTxt)
    
if __name__ == "__main__": 
    extractMeshSynonymDisease()
        