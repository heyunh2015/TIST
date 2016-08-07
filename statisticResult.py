# coding:utf-8
import support
import operator
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def extractMetricsToString(filesNameList, metrics):
    resCsv = ''
    for file in filesNameList:
        resCsvOfFile = file
        fp = open(file)
        for line in fp.readlines():
            lineArr = line.strip().split('\t')
            for metric in metrics:
                if str(lineArr[0]).strip()==metric and str(lineArr[2]).strip()=='all':
                    resCsvOfFile += ','+metric+','+str(lineArr[4])
        resCsv += resCsvOfFile +'\n'
    print resCsv
    
    return resCsv

def rankResults(filesNameList, metric):
    dicResultsMetric = {}
    for file in filesNameList:
        fp = open(file)
        for line in fp.readlines():
            lineArr = line.strip().split('\t')
            if str(lineArr[0]).strip()==metric and str(lineArr[2]).strip()=='all':
                dicResultsMetric[file] = float(lineArr[4])
                
    rankResultMetric = ''
    rankIndex=1
    for item in sorted(dicResultsMetric.iteritems(), key=operator.itemgetter(1), reverse=True):
        rankResultMetric += str(item[0])+' '+str(rankIndex)+' '+str(item[1]).replace('\n','')+'\n'
        rankIndex += 1
    print rankResultMetric
    return rankResultMetric

def plotResults(filesNameList, metric):
    listResultsMetric = []
    for file in filesNameList:
        fp = open(file)
        for line in fp.readlines():
            lineArr = line.strip().split('\t')
            if str(lineArr[0]).strip()==metric and str(lineArr[2]).strip()=='all':
                listResultsMetric.append(float(lineArr[4]))
    X = range(1,len(filesNameList)+1)
    plt.plot(X, listResultsMetric, 'r')
    plt.show()
    return 0

def threeDplotResults(filesNameList, metric):
    fig = plt.figure()
    ax = Axes3D(fig)
    X = range(1,11)
    Y = range(1,21)
    listResultsMetric = []
    for file in filesNameList:
        fp = open(file)
        for line in fp.readlines():
            lineArr = line.strip().split('\t')
            if str(lineArr[0]).strip()==metric and str(lineArr[2]).strip()=='all':
                listResultsMetric.append(float(lineArr[4]))
    ax.plot_wireframe(X, Y, listResultsMetric, rstride=1, cstride=1)
    return 0

if __name__ == "__main__": 
    #filesNameList = support.getResultFileNameFromFile('I:\\trec2016\\testMethodIn2015Data\\adjustPesudoRelevanceParameters\\eval', 
     #                                         'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\toBeAnalyizedResults\\adjustPesudoRelevanceFeedback.txt')
    filesNameList = support.getResultFileNameFromFolder('I:\\bibm2016\\experiments\\cds2015\\eval\\final2') 
    resCsv = extractMetricsToString(filesNameList, ['infNDCG', 'iP10'])
    support.saveFile(resCsv, 'I:\\bibm2016\\experiments\\cds2015\\resultStatistic\\final2.csv')
    rankResults(filesNameList, 'infNDCG')
    #plotResults(filesNameList, 'infNDCG')
    #threeDplotResults(filesNameList, 'infNDCG')