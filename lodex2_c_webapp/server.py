import tornado.ioloop
import tornado.web
import logging
import os
from operator import itemgetter
import pymongo as pm
import json


import pprint
import motor
# bad response recived from the endpoint > molte volte rispondono in xml

exclusion=[]



class MainHandler(tornado.web.RequestHandler):


    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        db = self.settings['db']
        cursor =db.lodex.ike.find({'ss':{'$exists':True}})
        res = []
        while (yield cursor.fetch_next):
            tmp  = cursor.next_object()
            res.append(tmp)
#         print res
        self.render('template', endpoints=res)


class GraphHandler(tornado.web.RequestHandler):
    def get(self, endpoint_id):
        self.render('prova2.html', endpoint_id = endpoint_id)
        
class DataHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, endpoint_id):
# #         self.db.EndPointSparql.find_one({'classNumber':{'$ne':None}, 'errors':{'$exists':False},'properties':{'$exists':True}},callback=self._on_response)
        db = self.settings['db']
        db.lodex.ike.find_one({'_id':int(endpoint_id)},callback=self._on_response)
        
    def _on_response(self,response,error):
         
#         json_data=open('static/flare.json')
#         data = json.load(json_data)
#         nodes = []
#         for 
#         response =yield db.Test.find_one({'_id':105})
        node = []
        invNode={}
        index = 0
        ss=response['ss']
        vocab=set('/'.join(a['p'].rsplit('/')[:-1]) for a in ss['attributes'])
        attributes={}
        
        for att in ss['attributes']:
#             vocab.add('/'.join(att['p'].rsplit('/')[:-1])
            if att['c'] not in attributes:
                attributes[att['c']]= [{'n':int(att['n']),'p':att['p']}]
            else:
                attributes[att['c']].append({'n':int(att['n']),'p':att['p']})
        
#         pprint.pprint(attributes)
        
#         for a in attributes:
#             pprint.pprint(attributes[a])
#             newlist = sorted(attributes[a], key=itemgetter('n'),reverse=True) 
#             pprint.pprint(newlist)
            
        for clas in ss['nodes']:
            vocab.add(extractVocab(clas['c']))
            att=[]
            if clas['c'] in attributes:
                
                att=[{'p':extrValue(a['p']),'n':float("{0:.2f}".format(float(float(a['n'])/float(clas['n'])))) if a['n'] > 0 else 0,'vocab':extractVocab(a['p']),'fullName':a['p']} for a in sorted(attributes[clas['c']], key=itemgetter('n'), reverse=True)]
                
                
#             print '/'.join(clas['c'].rsplit('/')[:-1])
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
            
                
#         pprint.pprint({'nodes':node,'links':edges})
#         pprint.pprint({'nodes':node})
# 
#         pprint.pprint(vocab)
        print 'lodex2c'
        self.write({'nodes':node,'links':edges,'vocab':list(vocab),'title':response['name'],'id':response['_id'],'uri':response['uri']})
        self.finish()

class IntensionalDataHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self ,s):
        

        id = self.get_argument("id",None)

        db.ike.find_one({'_id':int(id)},callback=self._on_response)
        
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
        print 'lodex2c'
        self.write({'nodes':node,'links':edges,'vocab':list(vocab),'title':response['nome'],'id':response['_id']})
        self.finish()


class IntensionalHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self,s):

        id = self.get_argument("id",None)

        
        
        db.ike.find_one({'_id':int(id)},callback=self._on_response)

    @tornado.web.asynchronous    
    def _on_response(self,response,error):

        if error:
            raise tornado.web.HTTPError(500)
        obj={}
        obj['s'] = self.get_argument("s",None)
        obj['p'] = self.get_argument("p",None)
        obj['o'] = self.get_argument("o",None)
        obj['id'] = self.get_argument("id",None)
        trovato = False
        if 'ik' in response:
            for i in response['ik']:
                #print extrValue(i['s'])
                if extrValue(i['s']) == obj['s']:
                    trovato=True
                    obj['ss']=i['s']                           
                if extrValue(i['s']) == obj['p']:
                    trovato=True
                    obj['pp']=i['s']        
                if extrValue(i['s']) == obj['o']:
                    trovato=True
                    obj['oo']=i['s']
                    
#         pprint.pprint(obj)
        empty=1
        if trovato:
            empty=0
        self.render('intensional.html',obj=obj,empty=empty )

    
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
    
    application = tornado.web.Application(handlers=[
    (r"/lodex2c", MainHandler),
    (r'/lodex2c/static/(.*)', tornado.web.StaticFileHandler, {'path': './static'}),
    (r"/lodex2c/([0-9]+)", GraphHandler),
    (r"/lodex2c/getData/([0-9]+)", DataHandler),
    (r"/lodex2c/intensional(.*)", IntensionalHandler),
    (r"/lodex2c/int/Data(.*)", IntensionalDataHandler),
#     (r"/lodex2/query", QueryDataHandler)
],
static_path=os.path.join(os.path.dirname(__file__), "static") ,db=db)
    port = 8890
    print 'Listening on http://localhost:', port
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
