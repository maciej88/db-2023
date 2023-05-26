from asyncio import run, sleep
from analysis_tools import get_companies, get_company_of_movie
from db_class import DbService

async def create_movie_companies():
    db = DbService()
    await db.initialize()

    movie_comps = get_company_of_movie()

    for mc, mcomp in enumerate(movie_comps):
        await db.upsert_movie_company(mcomp)
        if mc%100==0:
            print(f'insert movie companies in {mc/len(movie_comps)*100:.1f}% done')

    await sleep(1)

if __name__ == "__main__":
    run(create_movie_companies())