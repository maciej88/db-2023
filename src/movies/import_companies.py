from asyncio import run, sleep
from analysis_tools import get_companies, get_company_of_movie
from db_class import DbService

async def create_companies():
    db = DbService()
    await db.initialize()

    companies = get_companies()

    for c, comp in enumerate(companies):
        await db.upsert_prod_company(comp)
        if c% 100== 0:
            print(f'import companies in {c/len(companies) *100:.1f}% done')

    await sleep(1)

if __name__ == '__main__':
    run(create_companies())