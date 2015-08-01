from rdflib import Graph, URIRef, BNode, Literal
from rdflib.namespace import  RDFS, RDF
import pymongo as pm


client = pm.MongoClient()
dbLodex=client.lodex

end=dbLodex.ike.find_one({'_id':int(328)})

ss=end['css']

g = Graph()

print len(ss['edges'])

for a in ss['edges']:
    s=URIRef(a['s'])
    p=URIRef(a['p'])
    o=URIRef(a['o'])
    
    g.add((s,RDF.type,RDFS.Class))
    g.add((o,RDF.type,RDFS.Class))
    g.add((p,RDFS.range,o))
    g.add((p,RDFS.domain,s))
    
for a in ss['attributes']:
    s=URIRef(a['c'])
    p=URIRef(a['p'])
    g.add((p,RDFS.range,RDFS.Literal))
    g.add((p,RDFS.domain,s))
    
    
    
    
# print g.serialize(format='turtle')
# print len(g)


g.serialize(destination="328c.rdf", format="turtle")

