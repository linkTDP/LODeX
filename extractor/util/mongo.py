import pymongo as pm
import pprint
import datetime




class Endpoint():
    def __init__(self, e):
        if 'NCBO' in e:
            self.NCBO=e['NCBO']
        if '_id' in e:
            self.id=e['_id']
        if 'className' in e:
            self.className=e['className']
        if 'nome' in e:
            self.nome=e['nome']
        else:
            self.nome=None
        if 'uri' in e:
            self.uri=e['uri']
        if 'classNumber' in e:
            self.classNumber=e['classNumber']
        if 'instancesUnique' in e:
            self.instancesUnique=e['instancesUnique']
        if 'instances' in e:
            self.instances=e['instances']
        if 'classes' in e:
            self.classes=e['classes']
        if 'properties' in e:
            self.properties=e['properties']
        if 'error' in e:
            self.error=e['error']
        if 'log' in e:
            self.log=e['log']
        if 'propList' in e:
            self.propList=e['propList']
        if 'lock' in e:
            self.lock=e['lock']
        if 'version' in e:
            self.version=e['version']
        if 'acronym' in e:
            self.acronym=e['acronym']
        if 'ontology' in e:
            self.ontology=e['ontology']
        if 'ontology_prop' in e:
            self.acronym=e['ontology_prop']
        if 'triples' in e:
            self.triples=e['triples']
        
        
        
        
    def setError(self,error):
        self.errors=error    
    
    def setClassNumber(self,number):
        self.classNumber=number
        
    def setInstancesUnique(self,number):
        self.instancesUnique=number
        
    def setInstances(self,number):
        self.instances=number
        
    def setClasses(self,classes):
        self.classes=classes
    
    def setProperties(self,properties):
        self.properties=properties
        
    def toString(self):
        print 'NCBO             : '+str(self.NCBO)
        print '_id              :'+str(self.id)
        print 'className        :'+str(self.className)
        print 'nome             :'+str(self.nome)
        print 'uri              :'+str(self.uri)
        print 'classNumber      :'+str(self.classNumber)
        print 'instancesUnique  :'+str(self.instancesUnique)
        print 'instances        :'+str(self.instances)
        
    


def getAllEndopoinNoNcbo():
    client = pm.MongoClient()
    db=client.RDFstruct
    for e in db.EndPointSparql.find({'NCBO':False},timeout=False).sort("_id", 1):
        yield Endpoint(e)
        
def getAllEndopoinNoNcboNotTested():
    
    client = pm.MongoClient()
    db=client.RDFstruct
    for e in db.EndPointSparql.find({'classNumber':{'$exists':False}}):
        yield Endpoint(e)

def getAllEndopoinNoNcboNotError():
    client = pm.MongoClient()
    db=client.RDFstruct
    for e in db.EndPointSparql.find({'classNumber':{'$ne':None}, 'classes.0.instance':{'$exists':False}}):
        yield Endpoint(e)       
       
def getAllEnpointNoNCBOwithClassAndNInst():
    client = pm.MongoClient()
    db=client.RDFstruct
    for e in db.EndPointSparql.find({'classNumber':{'$ne':None}, 'classes.0.instance':{'$exists':True}},timeout=False):
        yield Endpoint(e)
        
def getAllEnpointNoNCBOwithClassAndNInstAndNotPrp():
    client = pm.MongoClient()
    db=client.RDFstruct
    for e in db.EndPointSparql.find({'classNumber':{'$ne':None}, 'classes.0.instance':{'$exists':True},
                                     'properties':{'$exists':False}}):
        yield Endpoint(e)
        
        
def getAllEnpointNoNCBOwithClassAndNInstAndPrp():
    client = pm.MongoClient()
    db=client.RDFstruct
    for e in db.EndPointSparql.find({'classNumber':{'$ne':None}, 'classes.0.instance':{'$exists':True},
                                     'properties':{'$exists':True}},timeout=False):
        if not hasattr(e, "errors"):
            ##########################
            # filtrare meglio        #
            ##########################
            yield Endpoint(e)       
        
def getEndpointByUrl(url):
    client = pm.MongoClient()
    db=client.RDFstruct
    if db.EndPointSparql.find_one({'uri':url}) is not None:
        return Endpoint(db.EndPointSparql.find_one({'uri':url}))
    else:
        return None


def updateError(endpoint):
    client = pm.MongoClient()
    client.RDFstruct.EndPointSparql.update({'_id':endpoint.id},{'$set':{'errors':endpoint.errors
                                                         }}) 

def updateEndpointInstanceClassNumber(endpoint):
    client = pm.MongoClient()
    if hasattr(endpoint,'classNumber') and hasattr(endpoint,'instances') and hasattr(endpoint,'instancesUnique'):
        client.RDFstruct.EndPointSparql.update({'_id':endpoint.id},{'$set':{'classNumber':endpoint.classNumber,
                                                         'instancesUnique':endpoint.instancesUnique,
                                                         'instances':endpoint.instances}})

def updateEndpointClasses(endpoint):
    client = pm.MongoClient()
    print endpoint.id
    client.RDFstruct.EndPointSparql.update({'_id':endpoint.id},{'$set':{'classes':endpoint.classes
                                                         }})        
        
#db.EndPointSparql.find({classNumber:{$exists:true}}).count()

def updateEndpointProp(endpoint):
    client = pm.MongoClient()
#     print endpoint.id
    client.RDFstruct.EndPointSparql.update({'_id':endpoint.id},{'$set':{'properties':endpoint.properties
                                                         }})  
def getEndpointByID(iid):
    client = pm.MongoClient()
    return Endpoint(client.RDFstruct.EndPointSparql.find_one({'_id':iid}))

def getNodesForGraph():
    client = pm.MongoClient()
    endpoint=client.RDFstruct.Test.find_one({'_id':163})
    node = []
    invNode={}
    index = 0
    for clas in endpoint['classes']:
        node.append({'name':clas['class'].rsplit('/')[len(clas['class'].rsplit('/'))-1]})
        invNode[clas['class'].rsplit('/')[len(clas['class'].rsplit('/'))-1]]=index
        index+=1
    edges = []
#     pprint.pprint(endpoint['properties'])
    for prop in endpoint['properties']:
        if prop['subject'].rsplit('/')[len(prop['subject'].rsplit('/'))-1] in invNode and prop['object'].rsplit('/')[len(prop['object'].rsplit('/'))-1] in invNode:
            edges.append({'source':invNode[prop['subject'].rsplit('/')[len(prop['subject'].rsplit('/'))-1]],
                      'target':invNode[prop['object'].rsplit('/')[len(prop['object'].rsplit('/'))-1]],
                      'value':1})
            
            
#         pprint.pprint()
    return {'nodes':node,'links':edges}


def getAllEndopoinNcbo():
    client = pm.MongoClient()
    db=client.RDFstruct
    for e in db.EndPointSparql.find({'NCBO':True},timeout=False).sort("_id", 1):
        yield Endpoint(e)



###################################################

#                TEST

###################################################

def startTest(endpoint):
    client = pm.MongoClient()
    if client.RDFstruct.Test.find_one({'_id':endpoint.id}) is not None:
        client.RDFstruct.Test.remove({'_id':endpoint.id})
    a={'_id':endpoint.id,
                             'NCBO':endpoint.NCBO,
                             'nome':endpoint.nome if endpoint.nome is not None else None,
                             'uri':endpoint.uri,
                             'log':[{'phase':'start','time':datetime.datetime.now()}],
                             'lock':True}
    client.RDFstruct.Test.insert(a)
    
def startCustom(endpoint):
    client = pm.MongoClient()
    if client.RDFstruct.logging.find_one({'_id':endpoint.id}) is not None:
        client.RDFstruct.logging.remove({'_id':endpoint.id})
    a={'_id':endpoint.id,
                             'NCBO':endpoint.NCBO,
                             'nome':endpoint.nome if endpoint.nome is not None else None,
                             'uri':endpoint.uri,
                             'log':[{'phase':'start','time':datetime.datetime.now()}],
                             'lock':True}
    client.RDFstruct.logging.insert(a)
    
def isCustomLocked(endpoint):
    client = pm.MongoClient()
    if client.RDFstruct.logging.find_one({'_id':endpoint.id}) is not None:
        return client.RDFstruct.logging.find_one({'_id':endpoint.id})['lock']
    else:
        return False

def addTestError(endpoint, error):
    if endpoint is not None:
        client = pm.MongoClient()
        client.RDFstruct.Test.update({'_id':endpoint.id},{'$push':{'error':error}})


def insertCustomLogging(endpoint, log):
    client = pm.MongoClient()
    if client.RDFstruct.logging.find_one({'_id':endpoint.id}) is None:
        startTest(endpoint)
    client.RDFstruct.logging.update({'_id':endpoint.id},{'$push':{'log':log}})

def insertCustomError(endpoint, error):
    client = pm.MongoClient()
    if client.RDFstruct.logging.find_one({'_id':endpoint.id}) is None:
        startTest(endpoint)
    client.RDFstruct.logging.update({'_id':endpoint.id},{'$push':{'error':error}})

def addTestLog(endpoint, log):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$push':{'log':log}})


def clearTest():
    client = pm.MongoClient()
    client.RDFstruct.Test.drop()

def updateEndpointClassesTest(endpoint,classes):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$set':{'classes':classes
                                                         }})    

def updateEndpointPropListTest(endpoint,propList):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$set':{'propList':propList
                                                         }})    

def getEndpointByUrlTest(url):
    client = pm.MongoClient()
    db=client.RDFstruct
    return Endpoint(db.Test.find_one({'uri':url}))




def updateEndpointPropertiesTest(endpoint, propAndNp):
    client = pm.MongoClient()
#     print endpoint.id
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$set':{'properties':propAndNp
                                                         }})  


def updateNumberClassesTest(endpoint, nClass):
    client = pm.MongoClient()
#     print endpoint.id
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$set':{'classNumber':nClass
                                                         }})  

def updateNumberTriplesTest(endpoint, ntri):
    client = pm.MongoClient()
#     print endpoint.id
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$set':{'triples':ntri
                                                         }})  

def updateNumberInstancesTest(endpoint, nIst):
    client = pm.MongoClient()
#     print endpoint.id
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$set':{'instances':nIst
                                                         }})  


def isEndpointByIDTest(iid):
    client = pm.MongoClient()
    if client.RDFstruct.Test.find_one({'_id':iid}) is not None:
        return True
    else:
        return False 

def getEndpointByIDTest(iid):
    client = pm.MongoClient()
    return Endpoint(client.RDFstruct.Test.find_one({'_id':iid}))

def pushEndpointPropertiesTest(endpoint, prop):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$push':{'properties':{'$each':prop}}})
    

def clearNotFinischedTest():
    client = pm.MongoClient()
    client.RDFstruct.Test.remove({'log':{'$not':{'$elemMatch':{'phase':'finish'}}}})
    
def getIfIsFinischedTest(idd):
    client = pm.MongoClient()
    return client.RDFstruct.Test.find({'_id':idd,'log':{'$elemMatch':{'phase':'finish'}}}).count()

def getIfIsFinischedCustom(idd):
    client = pm.MongoClient()
    return client.RDFstruct.logging.find({'_id':idd,'log':{'$elemMatch':{'phase':'finish'}}}).count()

def existTest(iid):
    client = pm.MongoClient()
    return client.RDFstruct.Test.find({'_id':iid}).count() > 0

def existTestAndIsNotLock(iid):
    client = pm.MongoClient()
    tmp = client.RDFstruct.Test.find_one({'_id':iid})
    if tmp is not None:
        end = Endpoint(tmp)
        if hasattr(end, "lock"):
            return not end.lock
        else:
            return False     
    else:
        return False
    
def isNotLock(iid):
    client = pm.MongoClient()
    tmp = client.RDFstruct.Test.find_one({'_id':iid})
    
    end = Endpoint(tmp)
    if hasattr(end, "lock"):
        return not end.lock
    else:
        return False     

def isNotLockCustom(iid):
    client = pm.MongoClient()
    tmp = client.RDFstruct.logging.find_one({'_id':iid})
    if tmp is not None:
        end = Endpoint(tmp)
        if hasattr(end, "lock"):
            return not end.lock
        else:
            return False
    else:
        return True
    
def clearLockTest():
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'lock':True},{'$set':{'lock':False}},multi=True)
    
def removeLockTest(iid):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':iid},{'$set':{'lock':False}})
    
def getTestCompleted():
    client = pm.MongoClient()
    for cur in client.RDFstruct.Test.find({'classNumber':{'$exists':True},
                                             'instances':{'$exists':True},
                                             'propList':{'$exists':True},
                                             'properties':{'$exists':True},
                                             'classes':{'$exists':True},
                                            'properties.0.count':{'$exists':True},
                                            'ontology_prop':{'$exists':False}},timeout=False):
        yield Endpoint(cur)

def getTestCompletedForOnto():
    client = pm.MongoClient()
    for cur in client.RDFstruct.Test.find({'propList':{'$exists':True},
                                             'classes':{'$exists':True},
                                            'ontology':{'$exists':False},
                                            'ontology_prop':{'$exists':False}},timeout=False):
        yield Endpoint(cur)
        
def insertTestOntoInExisting(onto,endpoint):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$set':{'ontology':onto}})

def insertTestOntoSet(ontSet,end):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':end.id},{'$set':{'ontology_to_lit':ontSet}})

def insertTestLeftCount(prop,endpoint):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$set':{'leftProp':prop}})
    
def insertTestLeftCountLit(prop,endpoint):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$set':{'leftProp_lit':prop}})
    
def pushTestLeftCount(prop,endpoint):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$push':{'leftProp':{'$each':prop}}})
    
def pushTestLeftCountLit(prop,endpoint):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$push':{'leftProp_lit':{'$each':prop}}})    

def insertTestRightCount(prop,endpoint):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$set':{'rightProp':prop}})

def pushTestRightCount(prop,endpoint):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$push':{'rightProp':{'$each':prop}}})
    
def insertTestOntoPropInExisting(onto,endpoint):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$set':{'ontology_prop':onto}})
    
def insertTestOntoPropSet(ontSet,end):
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':end.id},{'$set':{'ontology_prop_to_lit':ontSet}})
    
    
def findV2TestCompleted():
    client = pm.MongoClient()
    for cur in client.RDFstruct.Test.find({'classes':{'$exists':True},
                                             'leftProp':{'$exists':True},
                                             'propList':{'$exists':True},
                                        'rightProp':{'$exists':True}},timeout=False):
        yield cur
        
def findV2TestCompletedLoosly():
    client = pm.MongoClient()
    for cur in client.RDFstruct.Test.find({'classes':{'$exists':True},
                                             'leftProp':{'$exists':True},
                                             
                                        'rightProp':{'$exists':True}},timeout=False):
        yield cur
        
def GetCompletedV11():
    client = pm.MongoClient()
    for cur in client.RDFstruct.Test.find({'classes.0.nInstance':{'$exists':True},
                                             'leftProp.0.count':{'$exists':True},
                                            'leftProp_lit.0.count':{'$exists':True},
                                             'propList.0.nInstance':{'$exists':True},
                                        'rightProp.0.count':{'$exists':True}},timeout=False):
        yield cur
        
def getTestNumberError(end,name):
    client = pm.MongoClient()
    cur = client.RDFstruct.Test.find_one({'_id':end.id})
    if 'error' in cur:
        return len([err for err in cur['error'] if err['phase']==name])
    else:
        return 0
        
###################################################

#                Download prop

###################################################

def startTestTripleDown(endpoint):
    client = pm.MongoClient()
    if client.RDFstruct.TestTriple.find_one({'_id':endpoint['_id']}) is not None:
        client.RDFstruct.Test.remove({'_id':endpoint['_id']})
    client.RDFstruct.TestTriple.insert({'_id':endpoint['_id'],
                             'NCBO':endpoint['NCBO'],
                             'nome':endpoint['nome'],
                             'uri':endpoint['uri']})

def pushTestAutoundProp(idd,propp):
    client = pm.MongoClient()
    client.RDFstruct.TestTriple.update({'_id':idd},{'$push':{'aroundProp':propp}})
###################################################

#                NCBO

###################################################
 
def addEndpointNCBO(endpoint):
    client = pm.MongoClient()
    client.RDFstruct.ncbo.save({'_id':endpoint.id,'uri':endpoint.uri,'nome':endpoint.nome,'acronym':endpoint.acronym,'version':endpoint.version,
                                'classNumber':int(endpoint.classNumber),'instances':int(endpoint.instances),'classes':endpoint.classes,'propList':endpoint.propList})

# {'attribute':row[0],'table':row[1]}
def importKeyWordForNcbo(document):
    client = pm.MongoClient()
    for doc in document:
        client.RDFstruct.keyWord.save(doc)

def getTableName():
    client = pm.MongoClient()
    tableName = set()
    for cur in client.RDFstruct.keyWord.find():
        tableName.add(cur['table'])
    return tableName


def getColumnName():
    client = pm.MongoClient()
    columnName = []
    for cur in client.RDFstruct.keyWord.find():
        columnName.append({'table':cur['table'],'attribute':cur['attribute']})
    return columnName

def insertTestKeyword(results,collectionName):
    client = pm.MongoClient()
    collection = client.RDFstruct[collectionName]
    collection.insert(results)

def getAllKeyWord():
    client = pm.MongoClient()
    keyword = set()
    for cur in client.RDFstruct.keyWord.find():
        keyword.add(cur['table'])
        keyword.add(cur['attribute'])
    return keyword

def getTestCompletedForSecondPhase():
    client = pm.MongoClient()
    for cur in client.RDFstruct.Test.find({'propList':{'$exists':True},
                                             'classes':{'$exists':True}},timeout=False):
        yield Endpoint(cur)


    
def addIkeLog(endpoint, log):
    client = pm.MongoClient()
    client.RDFstruct.ike.update({'_id':endpoint.id},{'$push':{'log':log}})        
        
def insertTestIkE(onto,endpoint,iteration): 
    client = pm.MongoClient()
#     pprint.pprint(onto)
    client.RDFstruct.ike.update({'_id':endpoint.id},{'$set':{'ik':onto,'iteration':iteration}})
    
    
def insertIntensionalBulk(onto,endpoint): 
    client = pm.MongoClient()
#     pprint.pprint(onto)
    o=[{'s':o['s'],'p':o['p'],'o':o['o'],'id':endpoint.id} for o in onto]
    if len(o)>0:
        client.RDFstruct.intensional.insert(o)

def insertIkeInTest(onto,endpoint,iteration): 
    client = pm.MongoClient()
    pprint.pprint(onto)
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$set':{'ik':onto,'iteration':iteration}})
    
    
        
def startIkE(endpoint):
    client = pm.MongoClient()
    if client.RDFstruct.ike.find_one({'_id':endpoint.id}) is not None:
        client.RDFstruct.ike.remove({'_id':endpoint.id})
    client.RDFstruct.ike.insert({'_id':endpoint.id,
                             'NCBO':endpoint.NCBO,
                             'nome':endpoint.nome,
                             'uri':endpoint.uri,
                             'log':[{'phase':'start','time':datetime.datetime.now()}],
                             'lock':True
                             })
    
def getEndForIke():
    client = pm.MongoClient()
    db=client.RDFstruct
    for e in db.Test.find({'NCBO':False,'classes.0':{'$exists':1},'propList.0':{'$exists':1}},timeout=False).sort("_id", 1):
        yield Endpoint(e)
        
        
def addIkeError(endpoint, error):
    client = pm.MongoClient()
    client.RDFstruct.ike.update({'_id':endpoint.id},{'$push':{'error':error}})
    
def existIke(iid):
    client = pm.MongoClient()
    return client.RDFstruct.ike.find({'_id':iid}).count() > 0


def getAsServer():
    client = pm.MongoClient()
    db=client.RDFstruct
    ids=[e['_id'] for e in db.ike.find({'edges':{'$exists':True},'ingoing':{'$exists':True},'outgoing':{'$exists':True},'nodes':{'$exists':True}})]
#     pprint.pprint(ids)
        
    
    
    for e in db.Test.find({'_id':{'$in':ids}},timeout=False).sort("_id", 1):
        yield Endpoint(e)



def addTestCluster(co, endpoint):
    clu = [{'n':a['n'],'cluster':[b for b in a['cluster']]} for a in co]
    client = pm.MongoClient()
    client.RDFstruct.Test.update({'_id':endpoint.id},{'$set':{'cluster':clu}})


###############################
###############################
#        NEW                  #
###############################
###############################

def getLastRunById(idE):
    client = pm.MongoClient()
    return client.lodex.runInfo.find_one({'id':idE},sort=[("run", -1)])

def getExtByRunId(runId):
    client= pm.MongoClient()
    return [a for a in client.lodex.ext.find({'run':runId})]

def getClustByRunId(runId):
    client= pm.MongoClient()
    return [a for a in client.lodex.cluster.find({'run':runId})]


def startTestNew(endpoint):
    client = pm.MongoClient()
    currRun = client.lodex.runInfo.find_one({'id':endpoint['_id']},sort=[("run", -1)])
    currRunNumber = 1
    if currRun is not None:
        currRunNumber=currRun['run']+1
    a={'id':endpoint['_id'],
           'run':currRunNumber,
            'datasets':endpoint['datasets'] if 'dataset' in endpoint else None,
            'url':endpoint['url']}
    idRun = client.lodex.runInfo.insert(a)
    return idRun

def addTestLogNew(currentID, log):
    client = pm.MongoClient()
    client.lodex.runInfo.update({'_id':currentID},{'$push':{'log':log}})

def addTestErrorNew(curRun, error):
    if curRun is not None:
        client = pm.MongoClient()
        client.lodex.runInfo.update({'_id':curRun},{'$push':{'error':error}})


def updateNumberTriplesTestNew(runId, ntri):
    client = pm.MongoClient()
#     print endpoint.id
    client.lodex.runInfo.update({'_id':runId},{'$set':{'triples':ntri}})  

def updateNumberClassesTestNew(runId, nClass):
    client = pm.MongoClient()
#     print endpoint.id
    client.lodex.runInfo.update({'_id':runId},{'$set':{'classNumber':nClass}})
    
    
def updateNumberInstancesTestNew(runId, nIst):
    client = pm.MongoClient()
#     print endpoint.id
    client.lodex.runInfo.update({'_id':runId},{'$set':{'instances':nIst}})



def updateEndpointClassesTestNew(runId,classes):
    client = pm.MongoClient()
    client.lodex.runInfo.update({'_id':runId},{'$set':{'classes':classes}})

def getCurrentRunByIdTestNew(runId):
    client = pm.MongoClient()
    return client.lodex.runInfo.find_one({'_id':runId})
    
def updateEndpointPropListTestNew(runId,propList):
    client = pm.MongoClient()
    client.lodex.runInfo.update({'_id':runId},{'$set':{'propList':propList}})
    
def insertTestLeftCountNew(prop,runId,endId,kind):
    if len(prop) > 0:
        client = pm.MongoClient()
        client.lodex.ext.insert([{'id':endId,'run':runId,'kind':kind,'c':a['c'],'p':a['p'],'count':a['count']} for a in prop])

def addTestClusterNew(co, runId,endId):
    if len(co)>0:
        clu = [{'id':endId,'run':runId,'n':a['n'],'cluster':[b for b in a['cluster']]} for a in co]
        client = pm.MongoClient()
        client.lodex.cluster.insert(clu)

def getTestNumberErrorNew(runId,name):
    client = pm.MongoClient()
    cur = client.lodex.runInfo.find_one({'_id':runId})
    if 'error' in cur:
        return len([err for err in cur['error'] if err['phase']==name])
    else:
        return 0
    
    
def inserLodexDatasets(datasets):
    client = pm.MongoClient()
    client.lodex.endpoints.insert(datasets)

def getAllEndopoinLodex():
    client = pm.MongoClient()
    db=client.lodex
    for e in db.endpoints.find({},timeout=False).sort("_id", 1):
        yield e

def getByIdLodex(id):
    client = pm.MongoClient()
    db=client.lodex
    return db.endpoints.find_one({'_id':id})

def getLastIdEndpointsLodex():
    client = pm.MongoClient()
    lastEnd = client.lodex.endpoints.find_one({'_id':{'$exists':True}},sort=[("_id", -1)])
    if lastEnd is None:
        return 1
    else:
        return int(lastEnd['_id'])+1


def getNClassLodex(runId):
    client = pm.MongoClient()
    end=client.lodex.runInfo.find_one({'_id':runId})
    return len(end['classes']) if 'classes' in end else None


