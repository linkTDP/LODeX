import pymongo as pm
import pprint


class Query:
    
    def __init__(self,preQuery,postQuery,params):
        self.preQuery=preQuery
        self.postQuery=postQuery
        self.query=preQuery+postQuery
        self.params=params
        
    def getNCBO(self,dataset):
        return self.preQuery+" FROM <"+dataset+"> "+self.postQuery


class QueryGenerator:    
    
    def __init__(self,mongo=False):
        if mongo:
            self.queryRep=pm.MongoClient().RDFstruct.GenericQuery
    
    
    def getVoidQuery(self):
        for cur in self.queryRep.find():            
            yield Query(cur['prequery']+cur['postquery'],cur['parameters'])
        
    def getInstanceQuery(self):
        q = []
        q.append(Query("SELECT (COUNT (DISTINCT ?class) as ?no) )"),("( WHERE { [] a  ?class }",['?no']))
        q.append(Query("SELECT (COUNT(distinct ?s) AS ?no) "),(" { ?s a ?Class  }",['?no']))
        q.append(Query("SELECT (COUNT( ?s) AS ?no) "),("  { ?s a ?Class  }",['?no']))
        return q
    
    def getNumberClasses(self):
        return Query("SELECT (COUNT (DISTINCT ?class) as ?no)  ","  WHERE { ?s a  ?class }",['?no'])
    
    def getNumberInstances(self):
        return Query("SELECT (COUNT( ?s) AS ?no)  ","  { ?s a ?Class  }",['?no'])
    
    def testConnection(self):
        return Query(("SELECT ?s ?p ?o  "),("  WHERE {?s ?p ?o} LIMIT 1"),['?s','?p','?o'])
    
    def getClassesQuery(self):
        return Query(("SELECT DISTINCT ?class  "),("  WHERE { ?s a ?class}"),['?class'])
    
    def getClassesQueryPlusInstance(self):
        return Query(("SELECT DISTINCT ?class (COUNT(?s) as ?no)  "),("  WHERE {?s a ?class} GROUP BY ?class"),['?class'])
    
    def getInstacesByClasses(self,clas):
        return Query(("SELECT (COUNT (DISTINCT ?instance) as ?no)  "),("  WHERE { ?instance a  <"+clas+"> }"),['?no'])
    
    def getAllPropPlusNp(self):
        return Query(("SELECT ?SClass ?Popietry ?OClass (COUNT(?SInstance) as ?no)  "),("  {?SInstance a ?SClass. ?SInstance ?Popietry ?OInstance. ?OInstance a ?OClass.} GROUP BY ?SClass ?Popietry ?OClass",['SClass','?Popietry','?OClass','?no']))
    
    def getAllProp(self):
        return Query(("SELECT DISTINCT  ?SClass ?Popietry ?OClass  "),("  {?SInstance a ?SClass. ?SInstance ?Popietry ?OInstance. ?OInstance a ?OClass.} ",['SClass','?Popietry','?OClass']))
    
    def getPropBetClasses(self,clas):
        return Query(("SELECT DISTINCT ?Popietry ?OClass  "),("  {?SInstance a <"+clas+">. ?SInstance ?Popietry ?OInstance. ?OInstance a ?OClass.}",['?Popietry','?OClass']))

    def getPropBetClassesAndObject(self,clasS,clasO):
        return Query(("SELECT DISTINCT ?Popietry  "),("  {?SInstance a <"+clasS+">. ?SInstance ?Popietry ?OInstance. ?OInstance a <"+clasO+">.}",['?Popietry']))

    def getNumberUseProp(self,sClass,prop,oClass):
        return Query(("SELECT (COUNT(?SInstance) AS ?no)  "),("  {?SInstance a <"+sClass+">. ?SInstance <"+prop+"> ?OInstance. ?OInstance a <"+oClass+">.}",['?no']))

    def getPropertiesQuery(self):
        return Query(("SELECT DISTINCT ?prop  "),("  WHERE {?subject ?prop ?object}"),['?prop'])
        
    def getPropBetClassesObjectAndProp(self,sClass,prop,oClass):
        return Query(("SELECT ?SInstance  "),("  {?SInstance a <"+sClass+">. ?SInstance <"+prop+"> ?OInstance. ?OInstance a <"+oClass+">.} LIMIT 1",['?SInstance']))

    def getPropertiesAndNumUsage(self):
        return Query(("SELECT DISTINCT ?prop (count(?subject) AS ?no)  "),("  WHERE {?subject ?prop ?object} GROUP BY ?prop"),['?prop','?no'])
    
    def getDoubleExplorationFromClass(self,clas):
        return Query(("SELECT ?s ?bp ?fp ?o "),(" WHERE {?s ?bp <"+clas+">. <"+clas+"> ?fp ?o.}"),["?s","?bp", "?fp", "?o"])
        
    def getBackExplorationFromClass(self,clas):
        return Query(("SELECT ?s ?bp "),(" WHERE {?s ?bp <"+clas+">. }"),["?s","?bp"])

    def getForwardExplorationFromClass(self,clas):
        return Query(("SELECT  ?fp ?propType ?o "),(" WHERE { <"+clas+"> ?fp ?o. OPTIONAL {?fp a ?propType} }"),[ "?fp", "?o","?propType"])
    

#######################
#   Ontology extraction
######################

    def getOntoRelBySClassFiltered(self,clas):
        return Query(("SELECT ?p ?o "),(" WHERE { <"+clas+"> ?p ?o. FILTER (! isLITERAL(?o)) }"),[])

    def getOntoRelBySClassNotFiltered(self,clas):
        return Query(("SELECT ?p ?o "),(" WHERE { <"+clas+"> ?p ?o. FILTER (isLITERAL(?o)) }"),[])
    
    def getOntoRelBySClass(self,clas):
        return Query(("SELECT DISTINCT ?p ?o "),(" WHERE { <"+clas+"> ?p ?o. }"),[])

####################
#            V2
###################
    
    def getTestSPARQL(self):
        return Query(('SELECT COUNT(DISTINCT ?s) '),(' WHERE { <A> <B> ?s. } GROUP BY ?s LIMIT 1'),['?s'])

    def getPropListPlusCount(self):
        return Query(("SELECT ?p (COUNT(?s) as ?no) "),(" WHERE { ?s ?p ?o } GROUP BY ?p"),['?p','?no'])
    
    def getCountByProp(self,prop):
        return Query(("SELECT (COUNT(?s) as ?no) "),(" WHERE { ?s <"+prop+"> ?o. }"),['?no'])

    def getNumberOfTriples(self):
        return Query(("SELECT (COUNT(?s) as ?no) "),(" WHERE { ?s ?p ?o. } "),['?no'])

    def getLeftPropUsageWithCountNoLiteral(self,clas):
        return Query(("SELECT (COUNT(?p) as ?no) ?p "),(" WHERE { ?s a <"+clas+">. ?s ?p ?o. FILTER (!isLiteral(?o)) } GROUP BY ?p"),['?p','?no'])
    
    def getLeftPropUsageWithCountLiteral(self,clas):
        return Query(("SELECT (COUNT(?p) as ?no) ?p "),(" WHERE { ?s a <"+clas+">. ?s ?p ?o. FILTER (isLiteral(?o)) } GROUP BY ?p"),['?p','?no'])
    
    def getLeftPropCountNoLiteral(self,clas,prop):
        return Query(("SELECT (COUNT(?p) as ?no) "),(" WHERE { ?s a <"+clas+">. ?s <"+prop+"> ?o. FILTER (!isLiteral(?o)) }"),['?no'])
    
    def getLeftPropCountLiteral(self,clas,prop):
        return Query(("SELECT (COUNT(?p) as ?no) "),(" WHERE { ?s a <"+clas+">. ?s <"+prop+"> ?o. FILTER (isLiteral(?o)) }"),['?no'])
    
    def getRightPropUsageWithCount(self,clas):
        return Query(("SELECT (COUNT(?p) as ?no) ?p "),(" WHERE { ?s ?p ?o. ?o a <"+clas+">} GROUP BY ?p "),['?no','?p'])

    def getRightPropCount(self,clas,prop):
        return Query(("SELECT (COUNT(?p) as ?no) "),(" WHERE { ?s <"+prop+"> ?o. ?o a <"+clas+"> } GROUP BY ?p"),['?no'])
    
    def aroundProp(self,prop):
        return Query(("SELECT ?s ?o "),(" WHERE { ?s <"+prop+"> ?o. } LIMIT 10 "),["?s","?o"])
    
    def findPropBlankNode(self,clas):
        return Query(("SELECT ?p ?bp "),(" WHERE { ?s a <"+clas+">. ?s ?p ?b. ?b ?bp ?l. FILTER ( isBlank(?b) && isLiteral(?l) ) } GROUP BY ?p ?bp"),['?p','?bp'])
    
    #download dathub endpoint
    def ckanDownload(self):
        return Query(("SELECT distinct ?u "),("WHERE {?s a <http://purl.org/dc/terms/IMT>. ?s <http://www.w3.org/2000/01/rdf-schema#label> 'api/sparql'. ?a <http://purl.org/dc/terms/format> ?s. ?a <http://www.w3.org/ns/dcat#accessURL> ?u} "),[])
    
    def ckanDown2(self):
        return Query(("SELECT distinct ?u ?name ?label ?desc "),("WHERE {?s a <http://purl.org/dc/terms/IMT>. ?s <http://www.w3.org/2000/01/rdf-schema#label> 'api/sparql'. ?a <http://purl.org/dc/terms/format> ?s. ?a <http://www.w3.org/ns/dcat#accessURL> ?u. ?o <http://www.w3.org/ns/dcat#distribution> ?a. ?o <http://purl.org/dc/terms/title> ?name.?o <http://www.w3.org/2000/01/rdf-schema#label> ?label. ?o <http://purl.org/dc/terms/description> ?desc}"),[])
    
    def getDoubleInstantiation(self,clas):
        return Query(("SELECT ?c count(?s) "),(" WHERE { ?s a <"+clas+">. ?s a ?c. } GROUP BY ?c "),['?c','?no'])
    
    def getNInstantiation(self,setClases):
        queryBody=" WHERE { "
        for a in setClases:
            queryBody=queryBody+" ?s a <"+a+">. "
        queryBody=queryBody+" ?s a ?c. } GROUP BY ?c "
        return Query(("SELECT ?c count(?s) "),(queryBody),['?c','?no'])
    
####################
#    DBPEDIA
###################
    
    def getSubjectTriples(self,uri):
        return Query(("SELECT ?p ?o "),(" WHERE { <"+uri+"> ?p ?o. } "),['?p','?s'])
    
    def getObjectTriples(self,uri):
        return Query(("SELECT ?s ?p "),(" WHERE { ?s ?p <"+uri+">. } "),['?p','?o'])
    
    def getConnectedObj(self,distance,source,target):
        header="SELECT "
        body=" WHERE { "
        params=[]
        for e in range(distance+1):
            if e == 0:
                body=body+" <"+source+"> ?p"+str(e+1)+" ?e"+str(e+1)+" ."
            elif e == distance:
                body=body+" ?e"+str(e)+" ?p"+str(e+1)+" <"+target+"> ."
            else:
                body=body+" ?e"+str(e)+" ?p"+str(e+1)+" ?e"+str(e+1)+" ."
            header=header+" ?p"+str(e+1)+" ?e"+str(e+1)
            params.append('?e'+str(e+1))
            params.append('?p'+str(e+1))
        body=body+" }"
        return Query(header,body,params)
    
    def getConnectedObj2(self,distance,source,target):
        queryList=[]
        # firast way
        header="SELECT "
        body=" WHERE { "
        params=[]
        current=[]
        for e in range(distance+1):
            
            if e == 0:
                body=body+" <"+source+"> ?p"+str(e+1)+" ?e"+str(e+1)+" ."
                current.append(['s',"p"+str(e+1),"e"+str(e+1)])
            elif e == distance:
                body=body+" ?e"+str(e)+" ?p"+str(e+1)+" <"+target+"> ."
                current.append(["e"+str(e),"p"+str(e+1),"t"])
            else:
                body=body+" ?e"+str(e)+" ?p"+str(e+1)+" ?e"+str(e+1)+" ."
                current.append(["e"+str(e),"p"+str(e+1),"e"+str(e+1)])
            if e == distance:
                header=header+" ?p"+str(e+1)
            else:
                params.append('?e'+str(e+1))
                header=header+" ?p"+str(e+1)+" ?e"+str(e+1)
            params.append('?p'+str(e+1))
        body=body+" }"
        queryList.append((Query(header,body,params),current))
        #second way
        header="SELECT "
        body=" WHERE { "
        params=[]
        current=[]
        for e in range(distance+1):
            
            if e == 0:
                body=body+" <"+target+"> ?p"+str(e+1)+" ?e"+str(e+1)+" ."
                current.append(['t',"p"+str(e+1),"e"+str(e+1)])
            elif e == distance:
                body=body+" ?e"+str(e)+" ?p"+str(e+1)+" <"+source+"> ."
                current.append(["e"+str(e),"p"+str(e+1),"s"])
            else:
                body=body+" ?e"+str(e)+" ?p"+str(e+1)+" ?e"+str(e+1)+" ."
                current.append(["e"+str(e),"p"+str(e+1),"e"+str(e+1)])
            if e == distance:
                header=header+" ?p"+str(e+1)
            else:
                params.append('?e'+str(e+1))
                header=header+" ?p"+str(e+1)+" ?e"+str(e+1) 
            params.append('?p'+str(e+1))
        body=body+" }"
        queryList.append((Query(header,body,params),current))
        # change way in the middle
        for nodeInBetw in range(distance):
            header="SELECT "
            body1=" WHERE { "
            params=[]
            body2=" WHERE { "
            current1=[]
            current2=[]
            for e in range(distance+1):
                if e == 0:
                    body1=body1+" ?e"+str(e+1)+" ?p"+str(e+1)+" <"+source+"> ."
                    body2=body2+" <"+source+"> ?p"+str(e+1)+" ?e"+str(e+1)+" ."
                    current1.append(["e"+str(e+1),"p"+str(e+1),"s"])
                    current2.append(['s',"p"+str(e+1),"e"+str(e+1)])
                elif e == distance:
                    body1=body1+" ?e"+str(e)+" ?p"+str(e+1)+"  <"+target+"> ."
                    body2=body2+" <"+target+"> ?p"+str(e+1)+" ?e"+str(e)+" ."
                    current1.append(["e"+str(e),"p"+str(e+1),"t"])
                    current2.append(['t',"p"+str(e+1),"e"+str(e)])
                else:
                    if nodeInBetw >= e:
                        body1=body1+" ?e"+str(e)+" ?p"+str(e+1)+" ?e"+str(e+1)+" ."
                        body2=body2+" ?e"+str(e)+" ?p"+str(e+1)+" ?e"+str(e+1)+" ."
                        current1.append(["e"+str(e),"p"+str(e+1),"e"+str(e+1)])
                        current2.append(["e"+str(e),"p"+str(e+1),"e"+str(e+1)])
                    else:
                        body1=body1+" ?e"+str(e+1)+" ?p"+str(e+1)+" ?e"+str(e)+" ."
                        body2=body2+" ?e"+str(e+1)+" ?p"+str(e+1)+" ?e"+str(e)+" ."
                        current1.append(["e"+str(e+1),"p"+str(e+1),"e"+str(e)])
                        current2.append(["e"+str(e+1),"p"+str(e+1),"e"+str(e)])    
                if e == distance:
                    header=header+" ?p"+str(e+1)
                else:
                    params.append('?e'+str(e+1))
                    header=header+" ?p"+str(e+1)+" ?e"+str(e+1) 
                params.append('?p'+str(e+1))
            body1=body1+" }"
            body2=body2+" }"
            queryList.append((Query(header,body1,params),current1))
            queryList.append((Query(header,body2,params),current2))
        return queryList
    
def main():
    q = QueryGenerator()
    
    for a in q.getVoidQuery():
        pprint.pprint(a.query)
    
    
if __name__ == '__main__':
    main()




