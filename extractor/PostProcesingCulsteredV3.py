import util.mongo as mongo
import traceback
from itertools import chain, combinations
# import networkx as nx
import pymongo as pm
import sys
import time
import pprint

def powerset_generator_fr(i):
    for subset in chain.from_iterable(combinations(i, r) for r in range(len(i)+1)):
        yield frozenset(subset)



client = pm.MongoClient()
dbEnd=client.RDFstruct
dbLodex=client.lodex

rdfTypest="http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
virt="http://www.openlinksw.com/schemas/virtrdf"
owl="http://www.w3.org/2002/07/owl"
rdfs="http://www.w3.org/2000/01/rdf-schema"
 
"""
    Questa versione mantiene object e subject ma se una classe e' nel subset va as accumulare i path nella classe del supersets
    
    manca la sostizione degli attributi!!!!
    
"""  
 


    
    
def postProcForId(idEnd):

    
    end=mongo.getLastRunById(idEnd)
    
    print 'endpoint id : '+str(end['id'])+" loading..."
    
    errors=set()
    if 'error' in end:
        for err in end['error']:
            errors.add(err['phase'])
    
    extensional=mongo.getExtByRunId(end['_id'])
#         print 'here'
#         print extensional
    if 'test_connection' not in errors and 'Class' not in errors and 'NiByClass' not in errors and extensional is not None and len(extensional) > 0 :
        start_time = time.time()
        
        print 'endpoint id : '+str(end['id'])
        if 'name' in end:
            print end['name']
        
        print 'start time : '+str(start_time)
        
        classi=end['classes']
        propList=end['propList'] if 'propList' in end else None
        

        left=[a for a in extensional if a['kind'] == 0]
        left_lit=[a for a in extensional if a['kind'] == 1]
        right=[a for a in extensional if a['kind'] == 2]
     
        cluster = mongo.getClustByRunId(end['_id'])
#         if cluster is not None:
#             print len(cluster)

     
        clusterdSchemaSummary={}
        
        if len(cluster) > 0:
            print 'clustering alg'
            start_clust = time.time()
            """
            Clustering algorithm
            """
            
            
            print 'start Clustering'

            print 'n clust : '+str(len(cluster))
            
            #preprocesing:
            # remove classes of vrt, owl, rdfs
        
        
            clustSet=set()
            invIndx={}
            classSet=set()
        
            subClasses = set()
            superClass = set()
        
            
            for a in cluster:
                fail=False
                for b in a['cluster']:
                    if  virt in b or owl in b or rdfs in b:
                        fail = True
                if not fail:
                    nOccurence=a['n']
                    listClass=[]
                    for b in a['cluster']:
                        classSet.add(b)
                        listClass.append(b)
                    frSet=frozenset(listClass)
                    clustSet.add(frSet)
                    invIndx[frSet]=nOccurence
        
        
            for a in classi:
                if a['class'] in classSet:
                    cuClfrz=frozenset([a['class']])
                    clustSet.add(cuClfrz)
                    invIndx[cuClfrz]=a['nInstance']
        
        
            #pp.pprint(clustSet)
            #pp.pprint(invIndx)
            supersets=set()
        
            iteration = 0
        
            while len(clustSet) > 0:
            #    print iteration
            #    print len(clustSet)
                iteration = iteration + 1
                # find max lenght set
                maxL=0
                maxSet=None
                for a in clustSet:
                    if len(a) > maxL:
                        maxL=len(a)
                        maxSet=a
                supersets.add(maxSet)
                #compute powerSet
                powerset=set([a for a in powerset_generator_fr(maxSet)])
        
                clustSet.difference_update(powerset)
        
            #pp.pprint(len(supersets))
        
            print("--- %s seconds ---" % str(time.time() - start_time))
            
            
            # Here I find the the classes that are rapresentative of the cluster
            
            clustMappings={}

            for a in supersets:
                max=0
                maxClass=""
        
                for b in a:
                    if frozenset([b]) in invIndx and  int(invIndx[frozenset([b])]) > max:
                        max = int(invIndx[frozenset([b])])
                        maxClass = b
                
                for b in a:
                    if b <> maxClass:
                        clustMappings[b]=maxClass
                        subClasses.add(b)
                    else:
                        superClass.add(b)
                        
                        
        
        
            #pp.pprint(subClasses)
            #pp.pprint(superClass)
        
            superClass.difference_update(subClasses)
            
            
            """
            return superClass,supersets,invIndx
            """
            
            indexLeft={}
            
      
            propSet = set()
            
            
            
            
            tmpLeft=[]
            
            
        #print 'left pre :'+str(len(left))
            poper=[]
            for l in range(len(left)):
                   
        #         if left[l]['s'] in subClasses or left[l]['s'] in superClass:
        #             pprint.pprint(left[l])
                   
                if left[l]['p'] == rdfTypest or virt in left[l]['p'] or virt in left[l]['c'] or owl in left[l]['p'] or owl in left[l]['c'] or rdfs in left[l]['p'] or rdfs in left[l]['c']:
                    
                    poper.append(l)
                else:
                    if left[l]['c'] in subClasses:
#                         print 'sost'
#                         print left[l]['c']
                        tm={'c':clustMappings[left[l]['c']],'p':left[l]['p'],'count':left[l]['count']}
                        tmpLeft.append(tm)
#                         print left[l]['c']
                    else:
                        tmpLeft.append(left[l])
                    propSet.add(left[l]['p'])
            left=tmpLeft 

           
            tmpLeft=[]
            poper=[]
            #print 'right pre :'+str(len(right))
            for l in range(len(right)):

                if right[l]['p'] == rdfTypest or virt in right[l]['p'] or virt in right[l]['c'] or owl in right[l]['p'] or owl in right[l]['c']or rdfs in right[l]['p'] or rdfs in right[l]['c']:
                    
                    poper.append(l)
                else:
                    if right[l]['c'] in subClasses:
                        tm={'c':clustMappings[right[l]['c']],'p':right[l]['p'],'count':right[l]['count']}
                        tmpLeft.append(tm)
                    else:
                        tmpLeft.append(right[l])
                    propSet.add(right[l]['p'])
            right=tmpLeft           
         
            
            for l in range(len(left)):
                if left[l]['p'] in indexLeft:
                    indexLeft[left[l]['p']].append(l)
                else:
                    indexLeft[left[l]['p']]=[l]
                
            indexRight={}
                
            for l in range(len(right)):
                if right[l]['p'] in indexRight:
                    indexRight[right[l]['p']].append(l)
                else:
                    indexRight[right[l]['p']]=[l]
           
            
            edge = []
            clas = set()
            
            
            for key in propSet:
                if key in indexRight and key in indexLeft:
                    for l in indexLeft[key]:
                        for r in indexRight[key]:
                            if int(right[r]['count']) > 0 and int(left[l]['count']) > 0:
                                    
                                
                                clas.add(left[l]['c'])
                                clas.add(right[r]['c'])
                                if int(left[l]['count'])>=int(right[r]['count']):
                                    edge.append([left[l]['c'],left[l]['p'],right[r]['c'],int(right[r]['count'])])
                                    left[l]['count']=int(left[l]['count'])-int(right[r]['count'])
                                    right[r]['count']=0
                                else:
                                    edge.append([left[l]['c'],left[l]['p'],right[r]['c'],int(left[l]['count'])])
                                    right[r]['count']=int(right[r]['count'])-int(left[l]['count'])
                                    left[l]['count']=0
           
        #pprint.pprint(edge)
    
           
            poper=[]
            for l in range(len(left_lit)):
                if left_lit[l]['p'] == rdfTypest or virt in left_lit[l]['c'] or owl in left_lit[l]['c']  or rdfs in left_lit[l]['c'] or left_lit[l]['c'] in subClasses:
                    
                    poper.append(l)
                   
               
            for i in range(len(poper)):
                left_lit.pop(poper[i]-i)
            #print 'left_lit post :'+str(len(left_lit))
               
               
            attributes = []
               
            for c in clas:
                for at in left_lit:
                    if at['c'] == c:
                        attributes.append({'c':c,'p':at['p'],'n':at['count']})

            nodes=[]
            for c in clas:
                for tc in classi:
                    if tc['class']==c:
                        if c in superClass:
                            curCluster=[]
                            for currentCluster in cluster:
                                if c in currentCluster['cluster']:
                                    curCluster.append({'n':currentCluster['n'],'cluster':[b for b in currentCluster['cluster']]})
                            nodes.append({'c':c,'n':tc['nInstance'],'cluster':curCluster})
                        else:
                            nodes.append({'c':c,'n':tc['nInstance']})
            edges=[]            
            for e in edge:
                edges.append({'s':e[0],'p':e[1],'o':e[2],'n':e[3]})
                   
            outgoing=[]    
            for l in left:
                if int(l['count']) <> 0:
                    outgoing.append({'c':l['c'],'p':l['p'],'n':l['count']})
            ingoing=[]
            for r in right:
                if int(r['count'])<>0:
        #             print int(r['count'])==0
                    ingoing.append({'c':r['c'],'p':r['p'],'n':r['count']})
                   
            
            
            if len(superClass)>0:
                clusterdSchemaSummary={'nodes':nodes,'edges':edges,'attributes':attributes,'ingoing':ingoing,'outgoing':outgoing}
        
        
            print 'end clustering'
            print("--- %s seconds ---" % str(time.time() - start_clust))
        
        
        
        """
        *************************
        *************************
        without clustering algorithm
        """
        
        print 'start normal'
        start_normal = time.time()
        
        
        extensional=mongo.getExtByRunId(end['_id'])
        left=[a for a in extensional if a['kind'] == 0]
        left_lit=[a for a in extensional if a['kind'] == 1]
        right=[a for a in extensional if a['kind'] == 2]
        classi=end['classes']
        propSet = set()
        indexLeft={}
    
        #print 'left pre :'+str(len(left))
        poper=[]
        for l in range(len(left)):
            if left[l]['p'] == rdfTypest or virt in left[l]['p'] or virt in left[l]['c'] or owl in left[l]['p'] or owl in left[l]['c'] or rdfs in left[l]['p'] or rdfs in left[l]['c'] :
                poper.append(l)
            else:
                propSet.add(left[l]['p'])
        
        for i in range(len(poper)):
            left.pop(poper[i]-i)
        #print 'left post :'+str(len(left))
        
        
        poper=[]
        #print 'right pre :'+str(len(right))
        for l in range(len(right)):
            if right[l]['p'] == rdfTypest or virt in right[l]['p'] or virt in right[l]['c'] or owl in right[l]['p'] or owl in right[l]['c']or rdfs in right[l]['p'] or rdfs in right[l]['c']:
                poper.append(l)
            else:
                propSet.add(right[l]['p'])
                
        for i in range(len(poper)):
            right.pop(poper[i]-i)
        #print 'right post :'+str(len(right))   
         
             
         
        for l in range(len(left)):
            if left[l]['p'] in indexLeft:
                indexLeft[left[l]['p']].append(l)
            else:
                indexLeft[left[l]['p']]=[l]
         
        indexRight={}
         
        for l in range(len(right)):
            if right[l]['p'] in indexRight:
                indexRight[right[l]['p']].append(l)
            else:
                indexRight[right[l]['p']]=[l]
        
        #pprint.pprint(indexLeft) 
        #pprint.pprint(indexRight) 
         
        edge = []
        clas = set()
         
         
        for key in propSet:
            if key in indexRight and key in indexLeft:
                for l in indexLeft[key]:
                    for r in indexRight[key]:
                        if int(right[r]['count']) > 0 and int(left[l]['count']) > 0:
                            clas.add(left[l]['c'])
                            clas.add(right[r]['c'])
                            if int(left[l]['count'])>=int(right[r]['count']):
                                edge.append([left[l]['c'],left[l]['p'],right[r]['c'],int(right[r]['count'])])
                                left[l]['count']=int(left[l]['count'])-int(right[r]['count'])
                                right[r]['count']=0
                            else:
                                edge.append([left[l]['c'],left[l]['p'],right[r]['c'],int(left[l]['count'])])
                                right[r]['count']=int(right[r]['count'])-int(left[l]['count'])
                                left[l]['count']=0
        

        
        poper=[]
        for l in range(len(left_lit)):
            if left_lit[l]['p'] == rdfTypest or virt in left_lit[l]['c'] or owl in left_lit[l]['c']  or rdfs in left_lit[l]['c'] :
                poper.append(l)
            
        
        for i in range(len(poper)):
            left_lit.pop(poper[i]-i)
        #print 'left_lit post :'+str(len(left_lit))
        
        
        attributes = []
        
        for c in clas:
            for at in left_lit:
                if at['c'] == c:
                    attributes.append({'c':c,'p':at['p'],'n':at['count']})

        nodes=[]
        for c in clas:
            for tc in classi:
                if tc['class']==c:
                    nodes.append({'c':c,'n':tc['nInstance']})
        edges=[]            
        for e in edge:
            edges.append({'s':e[0],'p':e[1],'o':e[2],'n':e[3]})
            
        outgoing=[]    
        for l in left:
            if int(l['count']) <> 0:
                outgoing.append({'c':l['c'],'p':l['p'],'n':l['count']})
        ingoing=[]
        for r in right:
            if int(r['count'])<>0:
    #             print int(r['count'])==0
                ingoing.append({'c':r['c'],'p':r['p'],'n':r['count']})
                

        schemaSummary={'nodes':nodes,'edges':edges,'attributes':attributes,'ingoing':ingoing,'outgoing':outgoing}
        
        print 'end normal'
        print("--- %s seconds ---" % str(time.time() - start_normal))
        
        
        if dbLodex.ike.find({'_id':idEnd}).count() > 0:
            if not clusterdSchemaSummary:
                dbLodex.ike.update({'_id':idEnd},{'$set':{'ss':schemaSummary}})
            else:
                try:
                    dbLodex.ike.update({'_id':idEnd},{'$set':{'ss':schemaSummary,'css':clusterdSchemaSummary}})
                except:
                    print 'id to big'+str(idEnd)
            if 'instances' in end:
                dbLodex.ike.update({'_id':end['_id']},{'$set':{'instances':end['instances']}})
            if 'triples' in end:
                dbLodex.ike.update({'_id':end['_id']},{'$set':{'triples':end['triples']}})
            if 'classes' in end:
                dbLodex.ike.update({'_id':end['_id']},{'$set':{'classes':end['classes']}})
            if 'propList' in end:
                dbLodex.ike.update({'_id':end['_id']},{'$set':{'propList':end['propList']}})
                
        else:
            obj = {'_id':idEnd,'uri':end['url'],'ss':schemaSummary}
            if clusterdSchemaSummary:
                obj['css']=clusterdSchemaSummary
            if 'instances' in end:
                obj['instances']=end['instances']
            if 'triples' in end:
                obj['triples']=end['triples']
            if 'name' in end:
                obj['name']=end['name']
            if 'error' in end:
                obj['error']=end['error']
            if 'classes' in end:
                obj['classes']=end['classes']
            if 'propList' in end:
                obj['propList']=end['propList']
            
            
            try:  
                dbLodex.ike.insert(obj)
            except:
                var = traceback.format_exc()
                
                print sys.getsizeof(obj)
                if 'css' in obj:
                    print sys.getsizeof(obj['css'])
                
                print sys.getsizeof(obj['ss'])
                if 'css' in obj:
                    print sys.getsizeof(obj['css']['nodes'])
                print sys.getsizeof(obj['ss']['nodes'])
                
                print 'id +++'
                print obj['_id']
                print '----'
#          
            print 'total time'
            print("--- %s seconds ---" % str(time.time() - start_time))
