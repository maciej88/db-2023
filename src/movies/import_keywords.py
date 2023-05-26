
from asyncio import run

from analysis_tools import get_keywords
from db_class import DbService


async def create_keywords():
    db = DbService()
    await db.initialize()
    # await db.upsert_keyword(Keyword(333, "test"))

    keywords_ = get_keywords()

    print(f'all keywords: {len(keywords_)}')
    for k in keywords_:
        await db.upsert_keyword(k)


if __name__ == '__main__':
    run(create_keywords())