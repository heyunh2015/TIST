import support
def batchEvaluate(year, files):
    support.sampleEvalOnFolder('I:\\bibm2016\\experiments\\cds'+year+'\\evalTool',
                           'I:\\bibm2016\\experiments\\cds'+year+'\\qrel\\qrels-sampleval-'+year+'.txt',
                           'I:\\bibm2016\\experiments\\cds'+year+'\\result\\final3\\'+files,
                           'I:\\bibm2016\\experiments\\cds'+year+'\\eval\\final3\\'+files)
if __name__ == "__main__":  
    batchEvaluate('2016','weightBoe')
    