from asyncio import run, create_task, gather

from analysis_tools import *
from db_service import DbService
from model import Actor


async def create_movies():
    db = DbService()
    await db.initialize()

    mactors = get_movie_actors('data/tmdb_5000_credits.csv')
    print(f'all movieactors: {len(mactors)}')
    tasks = []
    for i, m in enumerate(mactors):
        tasks.append(create_task(db.upsert_movieactor(m)))
        if i % 100 == 0:
            print(f'import in {i / len(mactors) * 100:.1f}% done')
    await gather(*tasks)
    print('all done')


if __name__ == '__main__':
    run(create_movies())
