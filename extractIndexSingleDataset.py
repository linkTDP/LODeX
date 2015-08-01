import sys
import extractor.util.mongo as mongo
import extractor.SchemaExtractorTestV3 as se
import pymongo as pm


def main(argv):
    id=int(argv[0])
    end=mongo.getByIdLodex(id)
    se.ExtractSchema(end, True)


    print "creation mongo indexes"
    client = pm.MongoClient()

    client.lodex.ext.ensure_index('run')
    client.lodex.cluster.ensure_index('run')

    print "indexes created"

if __name__ == "__main__":
    main(sys.argv[1:])


