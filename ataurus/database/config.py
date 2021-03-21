INDEX_SETTINGS = {
  "settings": {
    "number_of_replicas": 1,
    "number_of_shards": 5,
    "index": {
      "analysis": {
        "analyzer": {

        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "text": {
        "type": "text"
      },
      "date": {
        "type": "date"
      }
    }
  }
}