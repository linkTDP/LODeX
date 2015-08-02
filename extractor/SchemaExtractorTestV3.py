import util.mongo as mongo
import logging
import util.queryGenerator as queryGenerator 
from SPARQLWrapper import SPARQLWrapper, XML # @UnresolvedImport
import traceback
import datetime
import pprint
import xml.dom.minidom
from urllib2 import addinfourl

x = logging.getLogger("logfun")
x.setLevel(logging.DEBUG)
h = logging.StreamHandler()
f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
h.setFormatter(f)
x.addHandler(h)
logfun = logging.getLogger("logfun")

def parseResponseForDatasetExtr(endpoint,results,phase,enableLog=True):
    if isinstance(results,xml.dom.minidom.Document):                   
        try:           
#             pretty_print = lambda data: '\n'.join([line for line in data.toprettyxml(indent=' '*2).split('\n') if line.strip()])
#             rtmp = parseString(pretty_print(results))
#             print rtmp.toprettyxml()
            res = results.getElementsByTagName('result')
            
            childcount=0
            for node in res:
                for binn in node.getElementsByTagName('binding'):
                    childcount = len(binn.childNodes)
            #si potrebbe fare con il valore mediano
            if childcount == 1:
                    res = [dict([(binn.attributes['name'].nodeValue, binn.firstChild.firstChild.nodeValue) for binn in node.getElementsByTagName('binding') if binn.firstChild.firstChild is not None]) for node in res]
            elif childcount == 3:
                    res = [dict([(binn.attributes['name'].nodeValue, binn.childNodes[1].firstChild.nodeValue) for binn in node.getElementsByTagName('binding')]) for node in res]    
#             print childcount
            if len(res)>0 or (len(res)==0 and results.getElementsByTagName('result') is not None):
                return res
            else:
                if enableLog:
                    errore = {"date":datetime.datetime.now(),"phase":phase, "traceback":results.toprettyxml()}
                    mongo.addTestError(endpoint, errore)
                return None
        except:
            logfun.exception("Something awful happened!")
            var = traceback.format_exc()
            if enableLog:
                errore = {"date":datetime.datetime.now(),"phase":phase,"traceback":var}
                mongo.addTestError(endpoint, errore)
    elif isinstance(results, addinfourl):
        print "addinfourl"
        logfun.exception("Something awful happened!")
        var = traceback.format_exc()
        if enableLog:    
            errore = {"date":datetime.datetime.now(),"phase":phase,"traceback":results.read()}
            mongo.addTestError(endpoint, errore)
        return None
    else:
        if enableLog:
            errore = {"date":datetime.datetime.now(),"phase":phase}
            mongo.addTestError(endpoint, errore)
        return None


def parseResponseWithType(runId,results,phase,enableLog=True,logCustom=False):
    if isinstance(results,xml.dom.minidom.Document):                   
        try:           
            res = results.getElementsByTagName('result')
#             print results.toprettyxml()
            childcount=0
            for node in res:
                for bin in node.getElementsByTagName('binding'):
                    childcount = len(bin.childNodes)
            #si potrebbe fare con il valore mediano
            if childcount == 1:
                    res = [[{binn.attributes['name'].nodeValue: binn.firstChild.firstChild.nodeValue,'type':binn.firstChild.tagName} for binn in node.getElementsByTagName('binding')] for node in res]
            elif childcount == 3:
                    res = [[{binn.attributes['name'].nodeValue: binn.childNodes[1].firstChild.nodeValue,'type':binn.childNodes[1].tagName} for binn in node.getElementsByTagName('binding')] for node in res]    
            
            if len(res)>0 or (len(res)==0 and results.getElementsByTagName('result') is not None):
#                 pprint.pprint(res)
                return res
            else:
                if enableLog:
                    errore = {"date":datetime.datetime.now(),"phase":phase, "traceback":results.toprettyxml()}
                    mongo.addTestErrorNew(runId, errore)
                return None
        except:
            logfun.exception("Something awful happened!")
            var = traceback.format_exc()
            if enableLog:
                errore = {"date":datetime.datetime.now(),"phase":phase,"traceback":var}
                mongo.addTestErrorNew(runId, errore)
    elif isinstance(results, addinfourl):
        print "addinfourl"
        logfun.exception("Something awful happened!")
        var = traceback.format_exc()
        if enableLog:    
            errore = {"date":datetime.datetime.now(),"phase":phase,"traceback":results.read()}
            mongo.addTestErrorNew(runId, errore)
        return None
    else:
        if enableLog:
            errore = {"date":datetime.datetime.now(),"phase":phase}
            mongo.addTestErrorNew(runId, errore)
        return None


def parseResponse(runId,results,phase,enableLog=True):
    """
    Return None if something goes wrong or the response.
    """
    if isinstance(results,xml.dom.minidom.Document):                   
#         print "dom.xml"
        try:           
#             pretty_print = lambda data: '\n'.join([line for line in data.toprettyxml(indent=' '*2).split('\n') if line.strip()])
#             rtmp = parseString(pretty_print(results))
#             print rtmp.toprettyxml()
            res = results.getElementsByTagName('result')
#             print results.toprettyxml()
            childcount=0
            for node in res:
                for binn in node.getElementsByTagName('binding'):
                    childcount = len(binn.childNodes)
            #si potrebbe fare con il valore mediano
            if childcount == 1:
                    res = [dict([(binn.attributes['name'].nodeValue, binn.firstChild.firstChild.nodeValue) for binn in node.getElementsByTagName('binding')]) for node in res]
            elif childcount == 3:
                    res = [dict([(binn.attributes['name'].nodeValue, binn.childNodes[1].firstChild.nodeValue) for binn in node.getElementsByTagName('binding')]) for node in res]    
            
            if len(res)>0 or (len(res)==0 and results.getElementsByTagName('result') is not None):
                return res
            else:
                if enableLog:
                    errore = {"date":datetime.datetime.now(),"phase":phase, "traceback":results.toprettyxml()}
                    mongo.addTestErrorNew(runId, errore)
                return None
        except:
            logfun.exception("Something awful happened!")
            var = traceback.format_exc()
            if enableLog:
                errore = {"date":datetime.datetime.now(),"phase":phase,"traceback":var}
                mongo.addTestErrorNew(runId, errore)
    elif isinstance(results, addinfourl):
        print "addinfourl"
        logfun.exception("Something awful happened!")
        var = traceback.format_exc()
        if enableLog:
            errore = {"date":datetime.datetime.now(),"phase":phase,"traceback":results.read()}
            mongo.addTestErrorNew(runId, errore)
        return None
    else:
        if enableLog:
            errore = {"date":datetime.datetime.now(),"phase":phase}
            mongo.addTestErrorNew(runId, errore)
        return None




## Test if and Enpoind i reacheble and the result of a quey is parsable
def testConnection(endpoint,q,sparql,runId):
    # START TEST CONNECTION TIME
    
    sparql.setQuery(q.testConnection().query)
    sparql.setReturnFormat(XML)
    print endpoint['_id']
    print q.testConnection().query
    try:
        results = sparql.queryAndConvert()
        if parseResponse(runId,results,"test_connection"):
            return True
        else:
            errore = {"date":datetime.datetime.now(),"phase":"test_connection"}
            mongo.addTestErrorNew(runId, errore)
            return False
    except:
        logfun.exception("Something awful happened!")
        var = traceback.format_exc()
        errore = {"date":datetime.datetime.now(),"phase":"test_connection","traceback":var}
        mongo.addTestErrorNew(runId, errore)
        return False



def adjLimitVirt(query, countResults):
    if countResults>0:
        query=query+" OFFSET "+str(countResults*10000)+" LIMIT 10000"
    return query


def downloadClassPlusInstance(endpoint, q, sparql,runId):
    sparql.setReturnFormat(XML)
    clasIntance=[]
    countResults=0
    try:
        while countResults >= 0:
            currQuery=adjLimitVirt(q.getClassesQueryPlusInstance().query,countResults)
            sparql.setQuery(currQuery)
            print endpoint['_id']
            print currQuery
            results = sparql.queryAndConvert()
            parsedRes=parseResponse(runId,results,'ClassPlusInstance')
            if parsedRes is not None:
                for clas in parsedRes:
                    clasIntance.append({'class':clas['class'],'nInstance':clas['no']})
    #             print 'len'+str(len(clasIntance))
                if len(parsedRes) == 10000:
                    countResults=countResults+1
                else:
                    countResults=-1    
            elif len(clasIntance)==0:
                errore = {"date":datetime.datetime.now(),"phase":"ClassPlusInstance"}
                mongo.addTestErrorNew(runId, errore)
                countResults=-1
    except:
        logfun.exception("Something awful happened!")
        var = traceback.format_exc()
        errore = {"date":datetime.datetime.now(),"phase":"ClassPlusInstance","traceback":var}
        mongo.addTestErrorNew(runId, errore)
    if len(clasIntance)>0:
#         print len(clasIntance)
        mongo.updateEndpointClassesTestNew(runId, clasIntance)
        return True
    else:
        errore = {"date":datetime.datetime.now(),"phase":"ClassPlusInstance"}
        mongo.addTestErrorNew(runId, errore)
        return False

def downloadPropListPlusCount(endpoint, q, sparql,runId):
    
    sparql.setReturnFormat(XML)
    countResults=0
    propCount=[]
    try:
        while countResults >= 0:
            currQuery=adjLimitVirt(q.getPropListPlusCount().query,countResults)
            sparql.setQuery(currQuery)
            print endpoint['_id']
            print currQuery
            results = sparql.queryAndConvert()
            parsedRes=parseResponse(runId,results,'PropListPlusCount')
            if parsedRes is not None:
                for pro in parsedRes:
                    propCount.append({'property':pro['p'],'nInstance':pro['no']})
                if len(parsedRes) == 10000:
                    countResults=countResults+1
                else:
                    countResults=-1
            else:
                errore = {"date":datetime.datetime.now(),"phase":"PropListPlusCount"}
                mongo.addTestErrorNew(runId, errore)
                countResults=-1
            
    except:
        logfun.exception("Something awful happened!")
        var = traceback.format_exc()
        errore = {"date":datetime.datetime.now(),"phase":"PropListPlusCount","traceback":var}
        mongo.addTestErrorNew(runId, errore)
    if len(propCount)>0:
        mongo.updateEndpointPropListTestNew(runId, propCount)
        return True
    else:
        errore = {"date":datetime.datetime.now(),"phase":"PropListPlusCount"}
        mongo.addTestErrorNew(runId, errore)
        return False


def downloadClasses(endpoint, q, sparql,runId):
    
    sparql.setReturnFormat(XML)
    countResults=0
    clases=[]
    try:
        while countResults >= 0:
            currQuery=adjLimitVirt(q.getClassesQuery().query,countResults)
            sparql.setQuery(currQuery)
            print endpoint['_id']
            print currQuery
            results = sparql.queryAndConvert()
            parsedRes=parseResponse(runId,results,'Class')
            if parsedRes is not None:
                for clas in parsedRes:
                    clases.append({'class':clas['class']})
                if len(parsedRes) == 10000:
                    countResults=countResults+1
                else:
                    countResults=-1
            else:
                errore = {"date":datetime.datetime.now(),"phase":"Class"}
                mongo.addTestErrorNew(runId, errore)
                countResults=-1
    except:
        logfun.exception("Something awful happened!")
        var = traceback.format_exc()
        errore = {"date":datetime.datetime.now(),"phase":"Class","traceback":var}
        mongo.addTestErrorNew(runId, errore)
    if len(clases)>0:
        mongo.updateEndpointClassesTestNew(runId, clases)
        return True
    else:
        errore = {"date":datetime.datetime.now(),"phase":"Class"}
        mongo.addTestErrorNew(runId, errore)
        return False


def downloadNumbInstances(endpoint, q, sparql,runId):
    sparql.setReturnFormat(XML)
    cur=mongo.getCurrentRunByIdTestNew(runId)
    classPlusInstance=[]
    for current in cur['classes']:        
        sparql.setQuery(q.getInstacesByClasses(current['class']).query)
        print endpoint['_id']
        print q.getInstacesByClasses(current['class']).query
        try:
            results = sparql.queryAndConvert()
            if parseResponse(runId,results,'NiByClass') is not None:
                if len(parseResponse(runId,results,'NiByClass'))>0:
                    classPlusInstance.append({'class':current['class'],'nInstance':int(parseResponse(runId,results,'NiByClass')[0]['no'])})
                else:
                    classPlusInstance.append({'class':current['class'],'nInstance':None})
            else:
                classPlusInstance.append({'class':current['class'],'nInstance':None})
                errore = {"date":datetime.datetime.now(),"phase":"NiByClass"}
                mongo.addTestErrorNew(runId, errore)
        except:
            classPlusInstance.append({'class':current['class'],'nInstance':None})
            logfun.exception("Something awful happened!")
            var = traceback.format_exc()
            errore = {"date":datetime.datetime.now(),"phase":"NiByClass","traceback":var}
            mongo.addTestErrorNew(runId, errore)
    if len(classPlusInstance) == len(cur['classes']):
        mongo.updateEndpointClassesTestNew(endpoint, classPlusInstance)
        return True
    else:
        return False

def downloadPropListCount(endpoint, q, sparql,runId):
    sparql.setReturnFormat(XML)
    cur=mongo.getCurrentRunByIdTestNew(runId)
    propPlusCount=[]
    for current in cur.propList:        
        sparql.setQuery(q.getCountByProp(current['property']).query)
        print endpoint['_id']
        print q.getCountByProp(current['property']).query
        try:
            results = sparql.queryAndConvert()
            if parseResponse(runId,results,'PropListCount') is not None:
#                 print parseResponse(runId,results,'PropListCount')
                if len(parseResponse(runId,results,'PropListCount'))>0:
                    propPlusCount.append({'property':current['property'],'count':int(parseResponse(runId,results,'PropListCount')[0]['no'])})
                else:
                    propPlusCount.append({'property':current['property'],'count':None})
            else:
                propPlusCount.append({'property':current['property'],'count':None})
                errore = {"date":datetime.datetime.now(),"phase":"PropListCount"}
                mongo.addTestErrorNew(runId, errore)
        except:
            propPlusCount.append({'property':current['property'],'count':None})
            logfun.exception("Something awful happened!")
            var = traceback.format_exc()
            errore = {"date":datetime.datetime.now(),"phase":"PropListCount","traceback":var,"prop":current['property']}
            mongo.addTestErrorNew(runId, errore)
            propPlusCount.append(current)
            
        ###### Break qui???
    if len(propPlusCount) == len(cur.propList):
        mongo.updateEndpointPropListTestNew(runId, propPlusCount)
# TODO che scriva quelli che scarica almeno 
        return True
    else:
        return False


def downloadNumberClasses(endpoint, q, sparql,runId):
    sparql.setQuery(q.getNumberClasses().query)
    sparql.setReturnFormat(XML)
    print endpoint['_id']
    print q.getNumberClasses().query
    try:
        results = sparql.queryAndConvert()
        if parseResponse(runId,results,'numb_classes') is not None and len(parseResponse(runId,results,'numb_classes'))>0:
            mongo.updateNumberClassesTestNew(runId,int(parseResponse(runId,results,'numb_classes')[0]['no']))
            return True
        else:
            errore = {"date":datetime.datetime.now(),"phase":"numb_classes"}
            mongo.addTestErrorNew(runId, errore)
            return False
    except:
        logfun.exception("Something awful happened!")
        var = traceback.format_exc()
        errore = {"date":datetime.datetime.now(),"phase":"numb_classes","traceback":var}
        mongo.addTestErrorNew(runId, errore)
        return False
    
def downloadNumberTriples(endpoint, q, sparql,runId):
    sparql.setQuery(q.getNumberOfTriples().query)
    sparql.setReturnFormat(XML)
    print endpoint['_id']
    print q.getNumberOfTriples().query
    try:
        results = sparql.queryAndConvert()
        if parseResponse(runId,results,'numb_triples') is not None and len(parseResponse(runId,results,'numb_triples'))>0:
            mongo.updateNumberTriplesTestNew(runId,int(parseResponse(runId,results,'numb_triples')[0]['no']))
            return True
        else:
            errore = {"date":datetime.datetime.now(),"phase":"numb_triples"}
            mongo.addTestErrorNew(runId, errore)
            return False
    except:
        logfun.exception("Something awful happened!")
        var = traceback.format_exc()
        errore = {"date":datetime.datetime.now(),"phase":"numb_triples","traceback":var}
        mongo.addTestErrorNew(runId, errore)
        return False


def downloadNumberInstances(endpoint, q, sparql,runId):
    sparql.setQuery(q.getNumberInstances().query)
    sparql.setReturnFormat(XML)
    print endpoint['_id']
    print q.getNumberInstances().query
    try:
        results = sparql.queryAndConvert()
        if parseResponse(runId,results,'numb_instances') is not None and len(parseResponse(runId,results,'numb_instances'))>0:
            mongo.updateNumberInstancesTestNew(runId,int(parseResponse(runId,results,'numb_instances')[0]['no']))
            return True
        else:
            errore = {"date":datetime.datetime.now(),"phase":"numb_instances"}
            mongo.addTestErrorNew(runId, errore)
            return False
    except:
        logfun.exception("Something awful happened!")
        var = traceback.format_exc()
        errore = {"date":datetime.datetime.now(),"phase":"numb_instances","traceback":var}
        mongo.addTestErrorNew(runId, errore)
        return False


def downloadPropList(endpoint,q,sparql,runId):
    sparql.setReturnFormat(XML)
    countResults=0
    prop = []
    try:
        while countResults >= 0:
            currQuery=adjLimitVirt(q.getPropertiesQuery().query,countResults)
            sparql.setQuery(currQuery)
            print endpoint['_id']
            print currQuery
            results = sparql.queryAndConvert()
            parsedRes=parseResponse(runId,results,'PropList')
            if parsedRes is not None:
                prop=[{'property':x['prop']} for x in parsedRes]
                if len(parsedRes) == 10000:
                    countResults=countResults+1
                else:
                    countResults=-1
            else:
                errore = {"date":datetime.datetime.now(),"phase":"PropList"}
                mongo.addTestErrorNew(runId, errore)
                countResults=-1
    except:
        logfun.exception("Something awful happened!")
        var = traceback.format_exc()
        errore = {"date":datetime.datetime.now(),"phase":"PropList","traceback":var}
        mongo.addTestErrorNew(runId, errore)
    if len(prop)>0:
        mongo.updateEndpointPropListTestNew(runId, prop)
        return True
    else:
        errore = {"date":datetime.datetime.now(),"phase":"PropList"}
        mongo.addTestErrorNew(runId, errore)
        return False
    


def downloadOnto(endpoint,q,sparql,runId):
    
    sparql.setReturnFormat(XML)
    onto = [] #result
    ontSet=[]
    ontoPro = []
    ontoProSet=[]
    # for iteration
    findedClasses=set()
    findedProperty=set()
    queriedClasses=set()
    queriedProperty=set()
#     for clas in endpoint.classes:
    end=mongo.getEndpointByIDTest(endpoint['_id'])
    # binding Class in subject classes
    if hasattr(end, 'classes'):
            findedClasses=set(clas['class'] for clas in end.classes)
    if hasattr(end, 'propList'):
            findedProperty=set(pro['property'] for pro in end.propList)
    print "** Extract Onto Classe"
    while len(findedClasses-queriedClasses)>0 or len(findedProperty-queriedProperty)>0:    
        print 'loop'
        print endpoint['_id']   
        for clas in findedClasses-queriedClasses:
            sparql.setQuery(q.getOntoRelBySClass(clas).query)
            try:
                results = sparql.queryAndConvert()
                queriedClasses.add(clas)
                if parseResponse(runId,results,'extract_onto_class') is not None and len(parseResponse(runId,results,'extract_onto_class'))>0:
                    print endpoint['_id']
                    print q.getOntoRelBySClass(clas).query
                    for cur in parseResponse(runId,results,'extract_onto_class'):
                        if cur[1]['type'] <> 'literal' and cur[1]['type'] <> 'bnode': #diverso bnode
                            
                            onto.append({'s':clas,'p':cur[0]['p'],'o':cur[1]['o']})
                            findedClasses.add(cur[1]['o'])
                            findedProperty.add(cur[0]['p'])
                        elif cur[1]['type'] == 'literal' :
                            findedProperty.add(cur[0]['p'])
                            if {'s':clas,'p':cur[0]['p']} not in ontSet:
                                ontSet.append({'s':clas,'p':cur[0]['p']})
            except:
                logfun.exception("Something awful happened!")
                var = traceback.format_exc()
                errore = {"date":datetime.datetime.now(),"phase":"extract_onto_class","traceback":var}
                mongo.addTestError(end, errore)

        # binding Prop in subject classes

        print "** Extract Onto prop"      
        print len(findedProperty-queriedProperty)
        for prop in findedProperty-queriedProperty:
            sparql.setQuery(q.getOntoRelBySClass(prop).query)
            try:
                results = sparql.queryAndConvert()
                queriedProperty.add(prop)
                if parseResponse(runId,results,'extract_onto_prop') is not None and len(parseResponse(runId,results,'extract_onto_prop'))>0:
                    print endpoint['_id']
                    print q.getOntoRelBySClass(prop).query
                    for cur in parseResponse(runId,results,'extract_onto_prop'):
                        if cur[1]['type'] <> 'literal' and cur[1]['type'] <> 'bnode': 
                            ontoPro.append({'s':prop,'p':cur[0]['p'],'o':cur[1]['o']})
                            findedClasses.add(cur[1]['o'])
                            findedProperty.add(cur[0]['p'])
                        elif cur[1]['type'] == 'literal' :
                            findedProperty.add(cur[0]['p'])
                            if {'s':prop,'p':cur[0]['p']} not in ontoProSet:
                                ontoProSet.append({'s':prop,'p':cur[0]['p']})
            except:
                logfun.exception("Something awful happened!")
                var = traceback.format_exc()
                errore = {"date":datetime.datetime.now(),"phase":"extract_onto_prop","traceback":var}
                mongo.addTestError(end, errore)

    mongo.insertTestOntoInExisting(onto,end)
    mongo.insertTestOntoSet(ontSet,end)
    mongo.insertTestOntoPropInExisting(ontoPro, end)
    mongo.insertTestOntoPropSet(ontoProSet,end)


def downloadPropLeftWithCount(endpoint,q,sparql,runId):
    sparql.setReturnFormat(XML)
    propOne = []
    curEnd=mongo.getCurrentRunByIdTestNew(runId)
    # binding Class left with count
    print "** Extract prop left no prop"
    anyError = False
    countError=0
    seqError=False
    if 'classes' in curEnd:        
        for clas in curEnd['classes']:
            countResults=0
            try:
                while countResults >= 0:
                    currQuery=adjLimitVirt(q.getLeftPropUsageWithCountNoLiteral(clas['class']).query,countResults)
                    sparql.setQuery(currQuery)

                    results = sparql.queryAndConvert()
                    parsedRes=parseResponse(runId,results,'prop_left_count')
                   
                    if parsedRes is not None and len(parsedRes)>0:
                        print endpoint['_id']
                        print currQuery
                        for cur in parsedRes:
                            if int(cur['no']) >0:
                                propOne.append({'c':clas['class'],'p':cur['p'],'count':cur['no']})
                        if seqError:
                            countError=0
                            seqError=False
                        if len(parsedRes) == 10000:
                            countResults=countResults+1
                        else:
                            countResults=-1
                    else:
                        countResults=-1   
            except:
                logfun.exception("Something awful happened!")
                var = traceback.format_exc()
                errore = {"date":datetime.datetime.now(),"phase":"prop_left_count","traceback":var,'class':clas['class']}
                anyError = True
                mongo.addTestErrorNew(runId, errore)
                seqError=True
                countError+=1
                if countError>=10:
                    mongo.addTestErrorNew(runId,{'phase':'prop_left_count','status':'aborted','time':datetime.datetime.now()})
                    print " ABORTED "
                    break
        mongo.insertTestLeftCountNew(propOne,runId,endpoint['_id'],0)
        
        #literal
        
        propOne=[]
        
        for clas in curEnd['classes']:
            countResults=0
            try:
                while countResults >= 0:
                    currQuery=adjLimitVirt(q.getLeftPropUsageWithCountLiteral(clas['class']).query,countResults)
                    sparql.setQuery(currQuery)

                    results = sparql.queryAndConvert()
                    parsedRes=parseResponse(runId,results,'prop_left_count_lit')
                   

                    if parsedRes is not None and len(parsedRes)>0:
                        print endpoint['_id']
                        print currQuery
                        for cur in parsedRes:
                            if int(cur['no']) >0:
                                propOne.append({'c':clas['class'],'p':cur['p'],'count':cur['no']})
                        if seqError:
                            countError=0
                            seqError=False
                        if len(parsedRes) == 10000:
                            countResults=countResults+1
                        else:
                            countResults=-1
                    else:
                        countResults=-1
            except:

                logfun.exception("Something awful happened!")
                var = traceback.format_exc()
                errore = {"date":datetime.datetime.now(),"phase":"prop_left_count_lit","traceback":var,'class':clas['class']}
                anyError = True
                mongo.addTestErrorNew(runId, errore)
                seqError=True
                countError+=1
                if countError>=10:
                    mongo.addTestErrorNew(runId,{'phase':'prop_left_count_lit','status':'aborted','time':datetime.datetime.now()})
                    print " ABORTED "
                    break
        mongo.insertTestLeftCountNew(propOne,runId,endpoint['_id'],1)
        
        
    else:
        errore = {"date":datetime.datetime.now(),"phase":"prop_left_count"}
        mongo.addTestErrorNew(runId, errore)
        # don't change anyError because he can't execute downloadPropLeftWithCountEasy
    return anyError

def downloadPropLeftWithCountEasy(endpoint,q,sparql,runId):
    sparql.setReturnFormat(XML)
    propOne = []
#     for clas in endpoint.classes:
    curEnd=mongo.getCurrentRunByIdTestNew(runId)
    # binding Class left with count
    print "** Extract prop left easy no lit"
    anyError = False
    if 'propList' in curEnd :
#         errorClass=[err['class'] for err in end.error if 'class' in err]
        for clas , prop in [(clas,prop['property']) for clas in [err['class'] for err in curEnd['error'] if 'class' in err] for prop in curEnd['propList']]:
            sparql.setQuery(q.getLeftPropCountNoLiteral(clas,prop).query)
            try:
                results = sparql.queryAndConvert()
                if parseResponse(runId,results,'prop_left_count_easy') is not None and len(parseResponse(runId,results,'prop_left_count_easy'))>0:
                    print endpoint['_id']
                    print q.getLeftPropCountNoLiteral(clas,prop).query
                    for cur in parseResponse(runId,results,'prop_left_count_easy'):
                        if int(cur['no']) >0:
                            propOne.append({'c':clas,'p':prop,'count':cur['no']})
            except:
                logfun.exception("Something awful happened!")
                var = traceback.format_exc()
                errore = {"date":datetime.datetime.now(),"phase":"prop_left_count_easy","traceback":var}
                anyError = True
                mongo.addTestErrorNew(runId, errore)
                if mongo.getTestNumberErrorNew(runId,'prop_left_count_easy')>=15:
                    print " ABORTED "
                    mongo.addTestErrorNew(runId,{'phase':'prop_left_count_easy','status':'aborted','time':datetime.datetime.now()})
                    break
#     pprint.pprint(propOne)
        if len(propOne)>0:
            mongo.insertTestLeftCountNew(propOne,runId,endpoint['_id'],0)
          
        #literal
        
        for clas , prop in [(clas,prop['property']) for clas in [err['class'] for err in  curEnd['error'] if 'class' in err] for prop in curEnd['propList']]:
            sparql.setQuery(q.getLeftPropCountLiteral(clas,prop).query)
            try:
                results = sparql.queryAndConvert()
                if parseResponse(runId,results,'prop_left_count_easy_lit') is not None and len(parseResponse(runId,results,'prop_left_count_easy_lit'))>0:
                    print endpoint['_id']
                    print q.getLeftPropCountLiteral(clas,prop).query
                    for cur in parseResponse(runId,results,'prop_left_count_easy_lit'):
                        if int(cur['no']) >0:
                            propOne.append({'c':clas,'p':prop,'count':cur['no']})
            except:
                logfun.exception("Something awful happened!")
                var = traceback.format_exc()
                errore = {"date":datetime.datetime.now(),"phase":"prop_left_count_easy_lit","traceback":var}
                anyError = True
                mongo.addTestErrorNew(runId, errore)
                if mongo.getTestNumberErrorNew(runId,'prop_left_count_easy_lit')>=15:
                    print " ABORTED "
#                     mongo.addTestLog(endpoint,{'phase':'prop_left_count_easy_lit','status':'aborted','time':datetime.datetime.now()})
                    break
#     pprint.pprint(propOne)
        if len(propOne)>0:
            mongo.insertTestLeftCountNew(propOne,runId,endpoint['_id'],1) 
          
#         mongo.addTestLog(endpoint,{'phase':'extract_onto_class','status':'finish','time':datetime.datetime.now()}) 
    return anyError

def downloadPropRightWithCount(endpoint,q,sparql,runId):
    sparql.setReturnFormat(XML)
    propOne = []
    curEnd=mongo.getCurrentRunByIdTestNew(runId)
    # binding Class left with count
    print "** Extract prop right"
    anyError = False
    if 'classes' in curEnd:        
        for clas in curEnd['classes']:
            countResults=0
            try:
                while countResults >= 0:
                    currQuery=adjLimitVirt(q.getRightPropUsageWithCount(clas['class']).query,countResults)
                    sparql.setQuery(currQuery)

                    results = sparql.queryAndConvert()
                    parsedRes=parseResponse(runId,results,'prop_right_count')
    
                    if parsedRes is not None and len(parsedRes)>0:
                        print endpoint['_id']
                        print currQuery
                        for cur in parsedRes:
                            if int(cur['no']) >0:
                                propOne.append({'c':clas['class'],'p':cur['p'],'count':cur['no']})
                        if len(parsedRes) == 10000:
                            countResults=countResults+1
                        else:
                            countResults=-1
                    else:
                        countResults=-1
            except:
                logfun.exception("Something awful happened!")
                var = traceback.format_exc()
                errore = {"date":datetime.datetime.now(),"phase":"prop_right_count","traceback":var,'class':clas['class']}
                anyError = True
                mongo.addTestErrorNew(runId, errore)
                if mongo.getTestNumberErrorNew(runId,'prop_right_count')>=15:
                    mongo.addTestErrorNew(runId,{'phase':'prop_right_count','status':'aborted','time':datetime.datetime.now()})
                    print " ABORTED "
                    break
        mongo.insertTestLeftCountNew(propOne,runId,endpoint['_id'],2)
    else:
        errore = {"date":datetime.datetime.now(),"phase":"prop_right_count"}
        mongo.addTestErrorNew(runId, errore)
        # don't change anyError because he can't execute downloadPropLeftWithCountEasy
    return anyError

def downloadPropRightWithCountEasy(endpoint,q,sparql,runId):
    sparql.setReturnFormat(XML)
    propOne = []
    curEnd=mongo.getCurrentRunByIdTestNew(runId)
    # binding Class left with count
    print "** Extract prop right easy"
    anyError = False
    if 'propList' in curEnd:
#         errorClass=[err['class'] for err in end.error if 'class' in err]
        for clas , prop in [(clas,prop['property']) for clas in [err['class'] for err in curEnd['error'] if 'class' in err] for prop in curEnd['propList']]:
            sparql.setQuery(q.getRightPropCount(clas,prop).query)
            try:
                results = sparql.queryAndConvert()
                if parseResponse(runId,results,'prop_right_count_easy') is not None and len(parseResponse(runId,results,'prop_right_count_easy'))>0:
                    print endpoint['_id']
                    print q.getRightPropCount(clas,prop).query
                    for cur in parseResponse(runId,results,'prop_right_count_easy'):
                        if int(cur['no']) >0:
                            propOne.append({'c':clas,'p':prop,'count':cur[0]['no']})
            except:
                logfun.exception("Something awful happened!")
                var = traceback.format_exc()
                errore = {"date":datetime.datetime.now(),"phase":"prop_right_count_easy","traceback":var}
                anyError = True
                mongo.addTestErrorNew(runId, errore)
                if mongo.getTestNumberErrorNew(runId,'prop_right_count_easy')>=15:
                    print " ABORTED "
                    mongo.addTestErrorNew(runId,{'phase':'prop_right_count_easy','status':'aborted','time':datetime.datetime.now()})
                    break
#     pprint.pprint(propOne)
    if len(propOne)>0:
        mongo.insertTestLeftCountNew(propOne,runId,endpoint['_id'],2)
#         mongo.addTestLog(endpoint,{'phase':'extract_onto_class','status':'finish','time':datetime.datetime.now()}) 
    return anyError


def downloadDoubleInst(endpoint, q, sparql,runId):
    sparql.setReturnFormat(XML)
    curEnd=mongo.getCurrentRunByIdTestNew(runId)
    # binding Class left with count
    print "** Extract double instantiation"
    couple=[]
    listOfSets=set()
    if 'classes' in curEnd:
#         errorClass=[err['class'] for err in end.error if 'class' in err]
        for clas in curEnd['classes']:
#             print ""
#             pprint.pprint(clas['class'])
            sparql.setQuery(q.getDoubleInstantiation(clas['class']).query)
            
            try:
                results = sparql.queryAndConvert()
                if parseResponse(runId,results,'double_inst',enableLog=False) is not None and len(parseResponse(runId,results,'double_inst',enableLog=False))>0:
                    
#                     print q.getDoubleInstantiation(clas['class']).query
                    for cur in parseResponse(runId,results,'double_inst',enableLog=False):
                        if cur['c'] <> clas['class']:
#                             print ""
#                             print str(clas['class'])+' - '+str(clas['nInstance'])
#                             print str(cur[0]['c'])+' - '+str(cur[1]['no'])
                            binding = ""
                            if 'callret-1' in cur:
                                binding='callret-1'
                            elif '.1' in cur:
                                binding='.1'
                            else:
                                print cur
                            tmpSet=set([clas['class'],cur['c']])
                            if frozenset(tmpSet) not in listOfSets:
                                listOfSets.add(frozenset(tmpSet))
                                couple.append({'cluster':tmpSet,'n':cur[binding]})

            except:
                logfun.exception("Something awful happened!")
                var = traceback.format_exc()
                errore = {"date":datetime.datetime.now(),"phase":"clustClasses","traceback":var}
                mongo.addTestErrorNew(runId, errore)

    return couple


def findClusterInstances(endpoint, q, sparql,cluster,runId):

    # binding Class left with count
    print "** Extract triple instantiation"
    couple=[]
    listOfSets=set()
    errorCount=0
    aborted=False
    print endpoint['_id']
    for clas in cluster:
        currentSet=clas['cluster']
#             print ""
#             pprint.pprint(clas['class'])
#         print q.getNInstantiation(currentSet).query
        sparql.setQuery(q.getNInstantiation(currentSet).query)
        try:
            results = sparql.queryAndConvert()
            if parseResponse(runId,results,'double_inst',enableLog=False) is not None and len(parseResponse(runId,results,'double_inst',enableLog=False))>0:
                print str(endpoint['_id'])+" getting result clustering"
#                     print q.getDoubleInstantiation(clas['class']).query
                for cur in parseResponse(runId,results,'double_inst',enableLog=False):
                    if cur['c'] not in currentSet:
#                             print ""
#                             print str(clas['class'])+' - '+str(clas['nInstance'])
#                             print str(cur[0]['c'])+' - '+str(cur[1]['no'])
                        binding = ""
                        if 'callret-1' in cur:
                            binding='callret-1'
                        elif u'.1' in cur:
                            binding='.1'
                        else:
                            print cur
                        
                        tmpSet=set(currentSet)
                        tmpSet.add(cur['c'])
#                         print listOfSets
                        if frozenset(tmpSet) not in listOfSets:
#                             print frozenset(tmpSet)
#                             print listOfSets
                            listOfSets.add(frozenset(tmpSet))
#                             print cur[1]
                            couple.append({'cluster':tmpSet,'n':cur[binding]})
#                 print couple
                        
                        
        except:
            errorCount=errorCount+1
            logfun.exception("Something awful happened!")
            var = traceback.format_exc()
            errore = {"date":datetime.datetime.now(),"phase":"clustClasses","traceback":var}
            mongo.addTestErrorNew(runId, errore)
        if errorCount > 20:
            aborted=True
            break

    return couple,aborted


def DoubleInstExtract(endpoint,q,sparql,runId):
    
    
    print endpoint['_id']
    co=downloadDoubleInst(endpoint,q,sparql ,runId)
#     pprint.pprint(co)
#     pprint.pprint(cu)
#     print ""
#     pprint.pprint(co)
    current = [c for c in co]
    while True:
        current,aborted = findClusterInstances(endpoint, q, sparql, current ,runId)
#         print current
        if len(current) == 0 or aborted:
            break
        else:
            co.extend(current)
    if len(co) > 0:        
        mongo.addTestClusterNew(co,runId,endpoint['_id'])
#     pprint.pprint(co)
#     if aborted:
#         mongo.addTestLog(endpoint,{'phase':'clustClasses','status':'aborted','time':datetime.datetime.now()})
#     else:
#         mongo.addTestLog(endpoint,{'phase':'clustClasses','status':'finish','time':datetime.datetime.now()})



def Inizialier(endpoint):
#     mongo.startTest(endpoint) # add Lock
    q = queryGenerator.QueryGenerator()
    sparql = SPARQLWrapper(endpoint['url'])
    sparql.setTimeout(300)
    
    return endpoint,q,sparql
    
def ExtractSchema(endpoint,clustering=False,nClassLimit=100):
#     print str(endpoint['_id'])+" - "+endpoint.nome+" - Test Connection "
    runId=mongo.startTestNew(endpoint) # add Lock
    q = queryGenerator.QueryGenerator()
    sparql = SPARQLWrapper(endpoint['url'])
    sparql.setTimeout(300)
    mongo.addTestLogNew(runId,{'phase':'test_connection','status':'start','time':datetime.datetime.now()})

    ## Test Connection
    if testConnection(endpoint,q,sparql,runId):
        mongo.addTestLogNew(runId,{'phase':'test_connection','status':'finish','time':datetime.datetime.now()})
        # number of triple
        mongo.addTestLogNew(runId,{'phase':'numb_triples','status':'start','time':datetime.datetime.now()})
        if downloadNumberTriples(endpoint,q,sparql,runId):
            mongo.addTestLogNew(runId,{'phase':'numb_triples','status':'finish','time':datetime.datetime.now()})
        # number of classes
        mongo.addTestLogNew(runId,{'phase':'numb_classes','status':'start','time':datetime.datetime.now()})
        if downloadNumberClasses(endpoint,q,sparql,runId):
            mongo.addTestLogNew(runId,{'phase':'numb_classes','status':'finish','time':datetime.datetime.now()})
        #number of instances
        mongo.addTestLogNew(runId,{'phase':'numb_instances','status':'start','time':datetime.datetime.now()})
        if downloadNumberInstances(endpoint,q,sparql,runId):
            mongo.addTestLogNew(runId,{'phase':'numb_instances','status':'finish','time':datetime.datetime.now()})
        # try to download list of class + instances
        mongo.addTestLogNew(runId,{'phase':'ClassPlusInstance','status':'start','time':datetime.datetime.now()}) 
        if not downloadClassPlusInstance(endpoint,q,sparql,runId):
            mongo.addTestLogNew(runId,{'phase':'Class','status':'start','time':datetime.datetime.now()})
            if downloadClasses(endpoint,q,sparql,runId):
                mongo.addTestLogNew(runId,{'phase':'Class','status':'finish','time':datetime.datetime.now()})
                print '**** NIsntanceByClass *****'
                mongo.addTestLogNew(runId,{'phase':'NiByClass','status':'start','time':datetime.datetime.now()})
                if downloadNumbInstances(endpoint,q,sparql,runId):
                    mongo.addTestLogNew(runId,{'phase':'NiByClass','status':'finish','time':datetime.datetime.now()})
        else:
            mongo.addTestLogNew(runId,{'phase':'ClassPlusInstance','status':'finish','time':datetime.datetime.now()})
        # try to download list of properties + uses
        
        print '**** Getting Properties  List *****'
        mongo.addTestLogNew(runId,{'phase':'PropListPlusCount','status':'start','time':datetime.datetime.now()})
        if not downloadPropListPlusCount(endpoint,q,sparql,runId):            
            mongo.addTestLogNew(runId,{'phase':'PropList','status':'start','time':datetime.datetime.now()})
            # try only prop
            if downloadPropList(endpoint,q,sparql,runId):
                mongo.addTestLogNew(runId,{'phase':'PropList','status':'finish','time':datetime.datetime.now()})
                # now download count for each prop
                mongo.addTestLogNew(runId,{'phase':'PropListCount','status':'start','time':datetime.datetime.now()})
                if downloadPropListCount(endpoint,q,sparql,runId):
                    mongo.addTestLogNew(runId,{'phase':'PropListCount','status':'finish','time':datetime.datetime.now()})
        else:
            mongo.addTestLogNew(runId,{'phase':'PropListPlusCount','status':'finish','time':datetime.datetime.now()})
                
#         if ike:
#             # download Ontological Info
#             mongo.addTestLogNew(runId,{'phase':'extract_onto','status':'start','time':datetime.datetime.now()})          
#             downloadIntensional(endpoint, q, sparql, False,runId)
#             mongo.addTestLogNew(runId,{'phase':'extract_onto','status':'finish','time':datetime.datetime.now()})
#             #TODO IMPROVING RICORSIVE SEARCH
        
        
        if mongo.getNClassLodex(runId) is not None and mongo.getNClassLodex(runId) < nClassLimit:
            """ extensional """
            # Extracting left right property
            #### left
            mongo.addTestLogNew(runId,{'phase':'prop_left_count','status':'start','time':datetime.datetime.now()})      
            if downloadPropLeftWithCount(endpoint,q,sparql,runId):
                mongo.addTestLogNew(runId,{'phase':'prop_left_count_easy','status':'start','time':datetime.datetime.now()})
                if not downloadPropLeftWithCountEasy(endpoint,q,sparql,runId):
                    mongo.addTestLogNew(runId,{'phase':'prop_left_count_easy','status':'finish','time':datetime.datetime.now()})
            else:
                mongo.addTestLogNew(runId,{'phase':'prop_left_count','status':'finish','time':datetime.datetime.now()})
            #### right
            mongo.addTestLogNew(runId,{'phase':'prop_right_count','status':'start','time':datetime.datetime.now()})
            if downloadPropRightWithCount(endpoint,q,sparql,runId):
                mongo.addTestLogNew(runId,{'phase':'prop_right_count_easy','status':'start','time':datetime.datetime.now()})
                if not downloadPropRightWithCountEasy(endpoint,q,sparql,runId):
                    mongo.addTestLogNew(runId,{'phase':'prop_right_count_easy','status':'finish','time':datetime.datetime.now()})
            else:
                mongo.addTestLogNew(runId,{'phase':'prop_right_count','status':'finish','time':datetime.datetime.now()})
            
            if clustering:
                """ Clustering ex """
                mongo.addTestLogNew(runId,{'phase':'clustClasses','status':'start','time':datetime.datetime.now()})
                DoubleInstExtract(endpoint,q,sparql,runId)
                mongo.addTestLogNew(runId,{'phase':'clustClasses','status':'finish','time':datetime.datetime.now()})
        else:
            print "extensional extraction skippet due to the high number of classes"
    ################## FINE
    mongo.addTestLogNew(runId,{'phase':'finish','time':datetime.datetime.now()})
    # removing Lock
    


def remDuplicatecoup(coup):
    cleaned=[]
    tmpC=[]
    for c in coup:
#         print c
        find=False
        if len(tmpC) >0:
            for a in tmpC:
                if (c['c1']==a['c1'] and c['c2']==a['c2']) or (c['c1']==a['c2'] and c['c2']==a['c1']):
                    find=True
            if not find:
                cleaned.append({'cluster':[c['c2'],c['c2']],'n':c['n']})
                tmpC.append(a)
        else:
            cleaned.append({'cluster':[c['c2'],c['c2']],'n':c['n']})
            tmpC.append(a)
    return cleaned

def generate_candidates(L, k):
    """Generate candidate set from `L` with size `k`"""
    candidates = set()
    for a in L:
        for b in L:
            union = a | b
            if len(union) == k and a != b:
                candidates.add(union)
    return candidates


