from asyncio import run, sleep
from analysis_tools import get_spoken_langs
from db_class import DbService

async def create_languages():
    db = DbService()
    await db.initialize()

    langs = get_spoken_langs('data/tmdb_5000_movies.csv')

    for l, lang in enumerate(langs):
        await db.upsert_language(lang)
        if l%100 == 0:
            print(f'import languages in {l/ len(langs)*100:.1f}% done')

    await sleep(1)

if __name__ == '__main__':
    run(create_languages())