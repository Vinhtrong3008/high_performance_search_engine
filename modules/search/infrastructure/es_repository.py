from typing import Dict, Any
from core.database.elasticsearch import es_client
from core.logging.logger import get_logger
from modules.search.domain.entities import ArticleDocument, SearchQuery
from modules.search.domain.repositories import SearchRepository

logger = get_logger(__name__)

class ElasticsearchSearchRepository(SearchRepository):
    INDEX_NAME = "articles_index"

    async def create_index_if_not_exists(self) -> None:
        client = es_client.client
        exists = await client.indices.exists(index=self.INDEX_NAME)
        if not exists:
            await client.indices.create(
                index=self.INDEX_NAME,
                body={
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0
                    },
                    "mappings": {
                        "properties": {
                            "url": {"type": "keyword"},
                            "title": {"type": "text", "analyzer": "standard"},
                            "content": {"type": "text", "analyzer": "standard"},
                            "summary": {"type": "text", "analyzer": "standard"},
                            "author": {"type": "keyword"},
                            "keywords": {"type": "keyword"},
                            "word_count": {"type": "integer"}
                        }
                    }
                }
            )
            logger.info("Elasticsearch index created successfully", index=self.INDEX_NAME)

    async def index_document(self, doc: ArticleDocument) -> str:
        await self.create_index_if_not_exists()
        client = es_client.client
        
        body = {
            "url": doc.url,
            "title": doc.title,
            "content": doc.content,
            "summary": doc.summary,
            "author": doc.author,
            "keywords": doc.keywords,
            "word_count": doc.word_count
        }
        
        response = await client.index(index=self.INDEX_NAME, document=body)
        logger.info("Document indexed successfully", id=response["_id"], url=doc.url)
        return response["_id"]

    async def search(self, query: SearchQuery) -> Dict[str, Any]:
        await self.create_index_if_not_exists()
        client = es_client.client

        from_offset = (query.page - 1) * query.size

        body = {
            "from": from_offset,
            "size": query.size,
            "query": {
                "multi_match": {
                    "query": query.keyword,
                    "fields": ["title^3", "summary^2", "content", "keywords^2"]
                }
            },
            "highlight": {
                "fields": {
                    "title": {},
                    "summary": {}
                }
            }
        }

        response = await client.search(index=self.INDEX_NAME, body=body)
        
        hits = response["hits"]["total"]["value"]
        results = []
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            source["id"] = hit["_id"]
            source["score"] = hit["_score"]
            source["highlights"] = hit.get("highlight", {})
            results.append(source)

        return {
            "total": hits,
            "page": query.page,
            "size": query.size,
            "items": results
        }