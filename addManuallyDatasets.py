import json
import sys
import lodex.util.mongo as mongo

def main(argv):
    file_name="datasets.json"
    if len(argv) > 0:
        file_name=argv[0]
    
    
    with open(file_name) as data_file:    
        data = json.load(data_file)["datasets"]
        for dat in data:
            id = mongo.getLastIdEndpointsLodex()
            ds={'_id':id,'name':dat['name'],'url':dat['url']}
            mongo.inserLodexDatasets(ds)


if __name__ == "__main__":
    main(sys.argv[1:])