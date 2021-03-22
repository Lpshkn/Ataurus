from elasticsearch_dsl import Document, Text, Keyword, Date


class Article(Document):
    title = Text()
    text = Text(required=True)
    date = Date()
    author = Keyword(required=True)

    class Index:
        name = 'articles'
        settings = {
            "number_of_shards": 5,
            "number_of_replicas": 1
        }
