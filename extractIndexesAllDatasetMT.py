from extractor import SchemaExtractorTestV3 as se
import threading
import time
from extractor.util import mongo         
import pymongo as pm

threads = []


# TODO choose number of thread

for a in mongo.getAllEndopoinLodex():
#     time.sleep(1)
    
    e= mongo.getLastRunById(a['_id'])
    logs=set()
    if e is not None:
        logs = set([l['phase'] for l in e['log']])
    
    if 'finish' not in logs:
    
            print '------------------'
            print len(threads)
        
            thread = threading.Thread(target=se.ExtractSchema, args=(a,False))
            thread.start()
        
            threads.append(thread)
            
            while len(threads) > 10:
                time.sleep(1)
                for t in threads:
                    if not t.isAlive():
                        print "Thread "+t.getName()+" terminated"
                        threads.remove(t)

# to wait until all three functions are finished

print "creation mongo indexes"



client = pm.MongoClient()

client.lodex.ext.ensure_index('run')
client.lodex.cluster.ensure_index('run')

print "indexes created"


print "Waiting..."

# for thread in threads:
#     thread.join()

print "Complete."



