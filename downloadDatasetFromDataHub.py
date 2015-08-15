from extractor import util
from SPARQLWrapper import SPARQLWrapper, XML # @UnresolvedImport
from extractor.SchemaExtractorTestV3 import parseResponseForDatasetExtr
from extractor.util import mongo

q = util.queryGenerator.QueryGenerator()
s = SPARQLWrapper("http://semantic.ckan.net/sparql")
s.setQuery(q.ckanDown2().query)
s.setReturnFormat(XML)

print "Extraction endpoints from Datahub\n"
print "sending sparql query to http://semantic.ckan.net/sparql\n"
results = s.queryAndConvert()
print "Parsing results\n"
# pprint.pprint(results.toprettyxml())
if parseResponseForDatasetExtr(None,results,"test_connection",False):
    endArr=[]
    endDIct={}
    for end in parseResponseForDatasetExtr(None,results,"test_connection",False):
        if 'name' in end:    
            if end['u'] in endDIct:
                tmp=endDIct[end['u']]
                tmp['name'].append(end['name'])
                tmp['label'].append(end['label'])
                if 'desc' in end:
                    tmp['desc'].append(end['desc'])
                else:
                    tmp['desc'].append(' ')
                endDIct[end['u']]=tmp
            else:
                endDIct[end['u']]={'name':[end['name']],'label':[end['label']],'desc':[end['desc']] if 'desc' in end else [' ']}
        
#     print endDIct
    
    
    datasets=[]
    count=mongo.getLastIdEndpointsLodex()
    for key in endDIct:
        ds={}
        if len(endDIct[key]['label']) > 1:
#             pprint.pprint(endDIct[key])
            labelSet=set(endDIct[key]['label'])
            globalName=reduce(lambda a,b: a if a>b else b,endDIct[key]['name'])
            ds={'url':key,'_id':count}
            count = count +1
            ds['datasets']=[]
            for a in labelSet:
                desc=""
                name=""
                for b in range(len(endDIct[key]['label'])):
                    if endDIct[key]['label'][b] == a:
                        if 'desc' in endDIct[key] and len(endDIct[key]['desc'][b]) > len(desc):
                            desc=endDIct[key]['desc'][b]
                        if len(endDIct[key]['name'][b]) > len(desc):
                            name=endDIct[key]['name'][b]
                
                ds['datasets'].append({'name':name,'label':a,'desc':desc})
            ds['name']=globalName          
        else:
            ds={'url':key,'_id':count,'name':endDIct[key]['name'][0]}
            count = count +1
            ds['datasets']=[{'name':endDIct[key]['name'][0],'label':endDIct[key]['label'][0],'desc':endDIct[key]['desc'][0] }]
        datasets.append(ds)
    print "Found "+str(len(datasets))+" datasets"
        #process and arr
        
        
        
        
        
    mongo.inserLodexDatasets(datasets)
    
