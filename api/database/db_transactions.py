from asyncpg.pool import Pool
import logging

logger = logging.getLogger(__name__)


class DatabaseTransactions:
    """Операции с базой данных"""

    def __init__(self, pool: Pool):
        self.pool = pool

    async def select(self, transaction: str, *args) -> dict or None:
        logger.debug('selecting one object')
        async with self.pool.acquire() as connection:
            if item := await connection.fetchrow(transaction.format(*args)):
                return dict(item)

    async def select_multiple(self, transaction: str, *args) -> list or None:
        logger.debug('selecting multiple objects')
        async with self.pool.acquire() as connection:
            if items := await connection.fetch(transaction.format(*args)):
                return [dict(item) for item in items]

    async def execute(self, transaction: str, *args):
        logger.debug('execute sql expression')
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(transaction.format(*args))
