from elasticsearch import AsyncElasticsearch
from core.config.settings import settings
from core.logging.logger import get_logger

logger = get_logger(__name__)

class ElasticsearchClient:
    client: AsyncElasticsearch = None

    @classmethod
    def connect(cls):
        cls.client = AsyncElasticsearch(hosts=[settings.ELASTICSEARCH_HOST])
        logger.info("Elasticsearch client initialized", host=settings.ELASTICSEARCH_HOST)

    @classmethod
    async def close(cls):
        if cls.client:
            await cls.client.close()
            logger.info("Elasticsearch connection closed")

es_client = ElasticsearchClient()