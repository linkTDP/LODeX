import tornado.ioloop
import tornado.web
import os
from operator import itemgetter



import pprint
import motor
from tornado import gen


exclusion=[]





class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('compatibility.html')
        
class MainHandlerOk(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')        


        
class IndexDatasetHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        exid=[a['_id'] for a in exclusion ]
#         pprint.pprint(exid)
        db = self.settings['db']#
        cursor = db.lodex.ike.find({'ss':{'$exists':True},'_id':{'$nin':exid}
                                            })
        res = []
        while (yield cursor.fetch_next):
            tmp  = cursor.next_object()
            res.append({'id':tmp['_id'],'name':tmp['name'] if 'name' in tmp else None,
                        'uri':tmp['uri'],'triples':tmp['triples'] if 'triples' in tmp else None,
                        'instances':tmp['instances'] if 'instances' in tmp else None,
                        'propCount':len(tmp['propList']) if 'propList' in tmp else None,
                        'classesCount':len(tmp['classes']) if 'classes' in tmp else None})
        self.content_type = 'application/json' 
        print len(res)
        self.write({'data':res})
        self.finish()

class IndexDatasetHandlerFull(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        exid=[a['_id'] for a in exclusion ]
#         pprint.pprint(exid)
        db = self.settings['db']#
        cursor = db.lodex.ike.find({'ss':{'$exists':True},'_id':{'$nin':exid}
                                            })
        res = []
        while (yield cursor.fetch_next):
            tmp  = cursor.next_object()
            res.append({'id':tmp['_id'],'name':tmp['name'] if 'name' in tmp else None,
                        'uri':tmp['uri'],'triples':tmp['triples'] if 'triples' in tmp else None,
                        'instances':tmp['instances'] if 'instances' in tmp else None,
                        'propCount':len(tmp['propList']) if 'propList' in tmp else None,
                        'classesCount':len(tmp['classes']) if 'classes' in tmp else None,
                        'classList':tmp['classes'] if 'classes' in tmp else None,
                        'propList':tmp['propList'] if 'propList' in tmp else None
                        })
        self.content_type = 'application/json' 
        self.write({'data':res})
        self.finish()            
    

class GraphHandler(tornado.web.RequestHandler):
    def get(self, endpoint_id):
        self.render('prova2.html', endpoint_id = endpoint_id)
        
class DataHandler(tornado.web.RequestHandler):
     
    @tornado.web.asynchronous
    def get(self, endpoint_id):
        db = self.settings['db']
        db.lodex.ike.find_one({'_id':int(endpoint_id)},callback=self._on_response)
        
    def _on_response(self,response,error):
        ss=response['ss']
        node = []
        invNode={}
        index = 0
        vocab=set('/'.join(a['p'].rsplit('/')[:-1]) for a in ss['attributes'])
        attributes={}
        
        for att in ss['attributes']:
#             vocab.add('/'.join(att['p'].rsplit('/')[:-1])
            if att['c'] not in attributes:
                attributes[att['c']]= [{'n':int(att['n']),'p':att['p']}]
            else:
                attributes[att['c']].append({'n':int(att['n']),'p':att['p']})
        
            
        for clas in ss['nodes']:
            vocab.add(extractVocab(clas['c']))
            att=[]
            if clas['c'] in attributes:
                
                att=[{'p':extrValue(a['p']),'n':float("{0:.2f}".format(float(float(a['n'])/float(clas['n'])))) if a['n'] > 0 else 0,'vocab':extractVocab(a['p']),'fullName':a['p']} for a in sorted(attributes[clas['c']], key=itemgetter('n'), reverse=True)]
                
                
            currentNode={'name':extrValue(clas['c']),'ni':int(clas['n']),'vocab':extractVocab(clas['c']),
                         'att':att,'fullName':clas['c']}
            custer=[]
            if 'cluster' in clas:
                for cl in clas['cluster']:
                    currentClust={'n':cl['n']}
                    currentClust['cluster']=[ {'vocab': extractVocab(c) ,'uri':c,'name':extrValue(c) }  for c in cl['cluster'] ]
                    custer.append(currentClust)
            if len(custer) > 0:
                currentNode['cluster']=custer
            
            node.append(currentNode)
            invNode[clas['c']]=index
            index+=1
        
        
#         pprint.pprint(invNode)
        edges = []
#         pprint.pprint(response["properties"])
        for prop in ss['edges']:
            if prop['s'] in invNode and prop['o'] in invNode:
                aggiunto=False
                for e in range(len(edges)):
                    if edges[e]['source']==invNode[prop['s']] and edges[e]['target']==invNode[prop['o']]:
                        edges[e]['label'].append({'np':int(prop['n']),  
                          'name':extrValue(prop['p']),
                          'vocab':extractVocab(prop['p']),
                          'fullName':prop['p']})
                        aggiunto=True
                if not aggiunto:
                    edges.append({'source':invNode[prop['s']],
                          'target':invNode[prop['o']],
                          'label':[{'np':int(prop['n']),  
                          'name':extrValue(prop['p']),
                          'vocab':extractVocab(prop['p']),
                          'fullName':prop['p']}]})
                
        for i in range(len(edges)):
            edges[i]['label']=sorted(edges[i]['label'], key=itemgetter('np')) 
            
                
        print 'lodex2'
        self.write({'nodes':node,'links':edges,'vocab':list(vocab),'title':response['name'],'id':response['_id'],'uri':response['uri']})
        self.finish()

class IntensionalDataHandler(tornado.web.RequestHandler):
     
    @tornado.web.asynchronous
    def get(self ,s):
        

        id = self.get_argument("id",None)

        db.lodex.ike.find_one({'_id':int(id)},callback=self._on_response)
        
    def _on_response(self,response,error):
        
        if error:
            raise tornado.web.HTTPError(500)
        obj=[]
        tmp={}
        tmp['s'] = self.get_argument("s",None)
        tmp['p'] = self.get_argument("p",None)
        tmp['o'] = self.get_argument("o",None)
        trovato = False
        step=0
        ik=[]
        if 'ik' in response:
            for i in response['ik']:
                #print extrValue(i['s'])
                if extrValue(i['s']) == tmp['s']:
                    trovato=True
                    tmp['ss']=i['s']
                    ik.append(i)                           
                if extrValue(i['s']) == tmp['p']:
                    trovato=True
                    tmp['pp']=i['s']
                    ik.append(i)        
                if extrValue(i['s']) == tmp['o']:
                    trovato=True
                    tmp['oo']=i['s']
                    ik.append(i)
        obj.append(tmp) 
        node = []
        invNode={}
        index = 0
        vocab=set()
        nodes=set()
        pprint.pprint(ik)
        for a in ik:
            nodes.add(a['s'])
            nodes.add(a['o'])

            
        for clas in nodes:
            vocab.add(extractVocab(clas))
            node.append({'name':extrValue(clas),'fullname':clas,'vocab':extractVocab(clas)})
            invNode[clas]=index
            index+=1
        
        edges = []
#         pprint.pprint(response["properties"])
        for prop in ik:
            if prop['s'] in invNode and prop['o'] in invNode:
                aggiunto=False
                for e in range(len(edges)):
                    if edges[e]['source']==invNode[prop['s']] and edges[e]['target']==invNode[prop['o']]:
                        edges[e]['label'].append({  
                          'name':extrValue(prop['p']),
                          'vocab':extractVocab(prop['p'])})
                        aggiunto=True
                if not aggiunto:
                    edges.append({'source':invNode[prop['s']],
                          'target':invNode[prop['o']],
                          'label':[{
                          'name':extrValue(prop['p']),
                          'vocab':extractVocab(prop['p'])}]})
                
               
#         pprint.pprint({'nodes':node,'links':edges})
# 
#         pprint.pprint(vocab)
#         
        print 'lodex2'
        self.write({'nodes':node,'links':edges,'vocab':list(vocab),'title':response['name'],'id':response['_id']})
        self.finish()


    
def extractVocab(uri):
    if len(uri.rsplit('/')[-1].split(':'))>1:
        return ':'.join(uri.rsplit(':')[:-1])
    elif len(uri.rsplit('/')[-1].split('#'))>1:
        return '#'.join(uri.rsplit('#')[:-1])
    else:
        return '/'.join(uri.rsplit('/')[:-1])

def extrValue(uri):
    if len(uri.rsplit('/')[-1].split(':'))>1:
        return uri.rsplit(':')[-1]
    elif len(uri.rsplit('/')[-1].split('#'))>1:
        return uri.rsplit('#')[-1]
    else:
        return uri.rsplit('/')[-1]

class QueryDataHandler:
    
    def prepare(self,request):
        pprint.pprint(request)
    
    def post(self,request):
        pprint.pprint(request)
#         data_json = tornado.escape.json_encode(self.request.arguments)
        pprint.pprint(self.request.body)

if __name__ == "__main__":
    db = motor.MotorClient()
    db2 = motor.MotorClient().lodex
    application = tornado.web.Application(handlers=[
    (r"/lodex2", MainHandler),
    (r"/lodex2/ok", MainHandlerOk),
    (r"/lodex2/index", IndexDatasetHandler),
    (r"/lodex2/indexComplete", IndexDatasetHandlerFull),
    (r'/lodex2/bower_components/(.*)', tornado.web.StaticFileHandler, {'path': './bower_components'}),
    (r'/bower_components/(.*)', tornado.web.StaticFileHandler, {'path': './bower_components'}),
    (r'/elements/(.*)', tornado.web.StaticFileHandler, {'path': './elements'}),
    (r'/lodex2/elements/(.*)', tornado.web.StaticFileHandler, {'path': './elements'}),
    (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': './js'}),
    (r'/lodex2/js/(.*)', tornado.web.StaticFileHandler, {'path': './js'}),
    (r"/lodex2/([0-9]+)", GraphHandler),
    (r"/lodex2/getData/([0-9]+)", DataHandler),
#     (r"/lodex2/query", QueryDataHandler)
],
static_path=os.path.join(os.path.dirname(__file__), "static") ,db=db)
    port = 8891
    print 'Listening on http://localhost:', port
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
