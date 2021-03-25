from elasticsearch import Elasticsearch, helpers
import json


class Elast():
    def __init__(self,index_name = 'news'):
        self.mapping = {
    "properties": {
        "title": {
            "type": "text",
            "analyzer": "ik_max_word"
        },
        "href": {
            "type": "keyword"
        },
        "infon": {
            "type": "text",
            "analyzer": "ik_max_word"
        },
        "times": {
            "type": "date",
            "format": "yyyy-MM-dd HH:mm:ss"
        },
        "topic": {
            "type": "keyword"
        },
        "source": {
            "type": "keyword"
        },
        "come_from": {
            "type": "keyword"
        }
    }
}
        self.es = Elasticsearch()
        self.index_name = index_name
        self.type = 'one_to_one'

    def import_data(self,datas):

        action = []

        for data in datas:
            action.append({
                "_index": self.index_name,
                "_op_type": "index",
                "_source":data
            })

        success, _ = helpers.bulk(self.es , action)
        print('success: ', success)
        return success

    def load_elasticsearch(self):
        #self.es.indices.delete(self.index_name) # 刪除index

        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name)
            #print('Index created!')

        if not self.es.indices.exists_type(index=self.index_name, doc_type=self.type):
            self.es.indices.put_mapping(
                index=self.index_name, doc_type=self.type, body=self.mapping, include_type_name=True)
            #print('Mappings created!')

        result = self.es.indices.get(index=self.index_name)  # index指定要get哪個index的資訊
        print("index and mappings is created",result)
        return result

        # success, _ = helpers.bulk(
        #     client=self.es, actions=self.read_data(), index=self.index_name, doc_type=self.type, ignore=400)
        # print('success: ', success)

    def search(self,ouary=""):
        reault = self.es.search(index=self.index_name,doc_type=self.type,body=ouary)
        reault = reault['hits']['hits']
        return reault#json.load(json.dumps(reault,indent=2))
if __name__ == '__main__':
    E = Elast()
    E.load_elasticsearch()

# result = E.es.indices.exists(index='google_news')
# print(result)