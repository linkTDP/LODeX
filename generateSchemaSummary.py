import pymongo as pm
from pprint import pprint
import extractor.PostProcesingCulsteredV3 as pp
import sys

client = pm.MongoClient()
dbEnd=client.lodex
dbLodex=client.lodex





def generateSSforAllEnd():

    ids=set([a['id'] for a in dbLodex.runInfo.find()])
    
    pprint(len(ids))
    
    for idEnd in ids:
        print idEnd
        pp.postProcForId(idEnd)
        
        
def generateSSforEndById(id):
    pp.postProcForId(id)
    
    
def main(argv):
    if 'all' == argv[0]:
        generateSSforAllEnd()
    else:
        print int(argv[0])
        generateSSforEndById(int(argv[0]))
    
    
if __name__ == "__main__":
    main(sys.argv[1:])