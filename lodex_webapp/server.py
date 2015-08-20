import tornado.ioloop
import tornado.web
import os
from operator import itemgetter


import pprint
import motor

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
        db = self.settings['db']
        db.lodex.ike.find_one({'_id':int(endpoint_id)},callback=self._on_response)
        
    def _on_response(self,response,error):

        node = []
        invNode={}
        index = 0
        ss=response['ss']
        vocab=set('/'.join(a['p'].rsplit('/')[:-1]) for a in ss['attributes'])
        attributes={}
        
        
        for att in ss['attributes']:
            if att['c'] not in attributes:
                attributes[att['c']]= [{'n':int(att['n']),'p':att['p']}]
            else:
                attributes[att['c']].append({'n':int(att['n']),'p':att['p']})

        for clas in ss['nodes']:
            vocab.add(extractVocab(clas['c']))
            att=[]
            if clas['c'] in attributes:
                
                att=[{'p':extrValue(a['p']),'n':float("{0:.2f}".format(float(float(a['n'])/float(clas['n'])))) if a['n'] > 0 else 0,'vocab':extractVocab(a['p']),'fullName':a['p']} for a in sorted(attributes[clas['c']], key=itemgetter('n'), reverse=True)]

            node.append({'name':extrValue(clas['c']),'ni':int(clas['n']),'vocab':extractVocab(clas['c']),
                         'att':att})
            invNode[extrValue(clas['c'])]=index
            index+=1
        
        edges = []

        for prop in ss['edges']:
            if extrValue(prop['s']) in invNode and extrValue(prop['o']) in invNode:
                aggiunto=False
                for e in range(len(edges)):
                    if edges[e]['source']==invNode[extrValue(prop['s'])] and edges[e]['target']==invNode[extrValue(prop['o'])]:
                        edges[e]['label'].append({'np':int(prop['n']),  
                          'name':extrValue(prop['p']),
                          'vocab':extractVocab(prop['p'])})
                        aggiunto=True
                if not aggiunto:
                    edges.append({'source':invNode[extrValue(prop['s'])],
                          'target':invNode[extrValue(prop['o'])],
                          'label':[{'np':int(prop['n']),  
                          'name':extrValue(prop['p']),
                          'vocab':extractVocab(prop['p'])}]})
                
        for i in range(len(edges)):
            edges[i]['label']=sorted(edges[i]['label'], key=itemgetter('np')) 
            
            
                
        #pprint.pprint({'nodes':node,'links':edges})

        #pprint.pprint(vocab)

        self.write({'nodes':node,'links':edges,'vocab':list(vocab),'title':response['name'] if 'name' in response else response['uri'],'id':response['_id']})
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
        #pprint.pprint(ik)
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
                
               
        #pprint.pprint({'nodes':node,'links':edges})

        #pprint.pprint(vocab)
        
        self.write({'nodes':node,'links':edges,'vocab':list(vocab),'title':response['name'] if 'name' in response else response['uri'],'id':response['_id']})
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

if __name__ == "__main__":
    db = motor.MotorClient()
    
    application = tornado.web.Application(handlers=[
    (r"/lodex", MainHandler),
    (r'/lodex/static/(.*)', tornado.web.StaticFileHandler, {'path': './static'}),
    (r"/lodex/([0-9]+)", GraphHandler),
    (r"/lodex/getData/([0-9]+)", DataHandler),
    (r"/lodex/intensional(.*)", IntensionalHandler),
    (r"/lodex/int/Data(.*)", IntensionalDataHandler),
],
static_path=os.path.join(os.path.dirname(__file__), "static") ,db=db)
    port = 8889
    print 'Listening on http://localhost:', port
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
