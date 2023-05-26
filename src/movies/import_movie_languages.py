from asyncio import run, sleep
from analysis_tools import get_movie_lang
from db_class import DbService
from model import MovieLanguage

async def create_movie_languages():
    db = DbService()
    await db.initialize()

    movie_langs = get_movie_lang('data/tmdb_5000_movies.csv')

    for ml, mlang in enumerate(movie_langs):
        await  db.upsert_movie_language(MovieLanguage(movie_id=mlang.movie_id,
                                                      lang_id=mlang.lang_id))
        if ml%100 == 0:
            print(f'import movie languages in {ml / len(movie_langs) * 100:.1f}% done')



if __name__ == "__main__":
    run(create_movie_languages())