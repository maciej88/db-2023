from __future__ import annotations

from asyncio import run, sleep

import asyncpg
from dotenv import load_dotenv
from os import getenv

from model import *

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')


class DbService:

    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5, min_size=15, max_size=20,
                                              server_settings={'search_path': SCHEMA})

        print('connected!')

    # actors

    async def get_actors(self, offset=0, limit=500) -> list[Actor]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from actors order by name offset $1 limit $2', offset, limit)
        return [Actor(**dict(r)) for r in rows]

    async def get_actor(self, actor_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from actors where actor_id=$1', actor_id)
        return Actor(**dict(row)) if row else None

    async def upsert_actor(self, actor: Actor) -> Actor:
        if actor.actor_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into actors(name) VALUES ($1) returning *",
                                                actor.name)
        elif await self.get_actor(actor.actor_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into actors(actor_id,name) VALUES ($1,$2) returning *",
                                                actor.actor_id, actor.name)
        else:
            actorFromDb = await self.get_actor(actor.actor_id)
            if actorFromDb == actor:
                return None

            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update actors set name=$2 where actor_id=$1 returning *""",
                                                actor.actor_id, actor.name)

        return Actor(**dict(row))

    # movies

    async def get_movies(self, offset=0, limit=500) -> list[Movie]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from movies order by title offset $1 limit $2', offset, limit)
        return [Movie(**dict(r)) for r in rows]

    async def get_movie(self, movie_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movies where movie_id=$1', movie_id)
        return Movie(**dict(row)) if row else None

    async def upsert_movie(self, movie: Movie) -> Movie:
        if movie.movie_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into movies(title) VALUES ($1) returning *",
                                                movie.title)
        elif await self.get_movie(movie.movie_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into movies(movie_id,title) VALUES ($1,$2) returning *",
                                                movie.movie_id, movie.title)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update movies set title=$2 where movie_id=$1 returning *""",
                                                movie.movie_id, movie.title)

        return Movie(**dict(row))

    async def get_movie_actor(self, movie_id: int, actor_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_actors where movie_id=$1 and actor_id=$2', movie_id,
                                            actor_id)
        return MovieActor(**dict(row)) if row else None

    async def get_movie_actors(self, offset=0, limit=500) -> list[Actor]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from movie_actors order by name offset $1 limit $2', offset, limit)
        return [Actor(**dict(r)) for r in rows]

    async def upsert_movie_actor(self, movie_actor: MovieActor) -> MovieActor:
        if await self.get_movie_actor(movie_actor.movie_id, movie_actor.actor_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    "insert into movie_actors(cast_id,movie_id,actor_id,credit_id,character,gender,position) VALUES ($1,$2, $3, $4, $5, $6, $7) returning *",
                    movie_actor.cast_id, movie_actor.movie_id, movie_actor.actor_id, movie_actor.credit_id,
                    movie_actor.character, movie_actor.gender, movie_actor.position)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """update movie_actors set movie_id=$2, actor_id=$3, credit_id=$4, character=$5, gender=$6, position=$7  where cast_id=$1 returning *""",
                    movie_actor.cast_id, movie_actor.movie_id, movie_actor.actor_id, movie_actor.credit_id,
                    movie_actor.character, movie_actor.gender, movie_actor.position)

        return MovieActor(**dict(row))


    async def get_genre(self, genre_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from genres where genre_id=$1', genre_id)
        return Genre(**dict(row)) if row else None

    async def get_genres(self, offset=0, limit=500) -> list[Genre]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from genres order by name offset $1 limit $2', offset, limit)
        return [Genre(**dict(r)) for r in rows]

    async def upsert_genre(self, genre: Genre) -> Genre:
        if genre.genre_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into genres(name) VALUES ($1) returning *",
                                                genre.name)
        elif await self.get_genre(genre.genre_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into genres(genre_id,name) VALUES ($1,$2) returning *",
                                                genre.genre_id, genre.name)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update genres set name=$2 where genre_id=$1 returning *""",
                                                genre.genre_id, genre.name)

        return Genre(**dict(row))

    async def get_movie_genre(self, genre_id: int, movie_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_genres where genre_id=$1 and movie_id=$2', genre_id, movie_id)
        return MovieGenre(**dict(row)) if row else None

    async def get_movie_genres(self, offset=0, limit=500) -> list[Genre]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from movie_genres order by name offset $1 limit $2', offset, limit)
        return [MovieGenre(**dict(r)) for r in rows]

    async def upsert_movie_genre(self, genre_id, movie_id) -> MovieGenre:
        if genre_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into movie_genres(genre_id) VALUES ($1) returning *",
                                                genre_id)
        elif await self.get_movie_genre(genre_id, movie_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into movie_genres(genre_id,movie_id) VALUES ($1,$2) returning *",
                                                genre_id, movie_id)
        else:
            # update

            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update movie_genres set genre_id=$2 where movie_id=$1 returning *""",
                                                movie_id, genre_id)

        return MovieGenre(**dict(row))

    async def get_pcountry(self, iso: str):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('SELECT * FROM pcountries WHERE iso_3166_1=$1', iso)
        return PCountry(**dict(row)) if row else None


    async def get_pcountries(self, offset=0, limit=500) -> list[PCountry]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('SELECT * FROM pcountries ORDER BY name OFFSET $1 LIMIT $2', offset, limit)
        return [PCountry(**dict(r)) for r in rows]


    async def upsert_pcountry(self, pcountry: PCountry) -> PCountry:
        if pcountry.iso_3166_1 is None:
            raise ValueError("PCountry must have iso_3166_1 value.")

        async with self.pool.acquire() as connection:
            if pcountry.name is None:
                row = await connection.fetchrow(
                    "insert into pcountries(iso_3166_1) VALUES ($1) returning *",
                    pcountry.iso_3166_1,
                )
            else:
                row = await connection.fetchrow(
                    "insert into pcountries(iso_3166_1, name) VALUES ($1, $2) "
                    "on conflict (iso_3166_1) do update set name = $2 returning *",
                    pcountry.iso_3166_1,
                    pcountry.name,
                )

        return PCountry(**dict(row))

    async def get_movie_pcountry(self, movie_id: int, iso_3166_1: str):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_pcountries where movie_id=$1 and iso_3166_1=$2', movie_id, iso_3166_1)
        return MoviePCountry(**dict(row)) if row else None

    async def get_movie_pcountries(self, offset=0, limit=500) -> list[MoviePCountry]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from movie_pcountries order by movie_id, iso_3166_1 offset $1 limit $2', offset, limit)
        return [MoviePCountry(**dict(r)) for r in rows]

    async def upsert_movie_pcountry(self, movie_pcountry: MoviePCountry) -> MoviePCountry:
        movie_id = movie_pcountry.movie_id
        iso_3166_1 = movie_pcountry.iso_3166_1
        if await self.get_movie_pcountry(movie_id, iso_3166_1) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into movie_pcountries(movie_id, iso_3166_1) VALUES ($1,$2) returning *",
                                                movie_id, iso_3166_1)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update movie_pcountries set movie_id=$1 where iso_3166_1=$2 returning *""",
                                                movie_id, iso_3166_1)

        return MoviePCountry(**dict(row))

    async def get_crew(self, crew_id: int) -> Crew | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from crew where crew_id=$1', crew_id)
        return Crew(**dict(row)) if row else None

    async def get_crews(self, offset=0, limit=500) -> list[Crew]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from crew order by name offset $1 limit $2', offset, limit)
        return [Crew(**dict(row)) for row in rows]

    async def upsert_crew(self, crew: Crew) -> Crew:
        c = crew
        if await self.get_crew(c.crew_id) is None:
            #insertion:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('insert into crew('
                                               'crew_id, gender, name) '
                                               'values ($1, $2, $3) returning *',
                                               c.crew_id, c.gender, c.name)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update crew set 
                                                crew_id=$1, gender=$2, name=$3 
                                                returning *""",
                                                c.crew_id, c.gender, c.name)
        return Crew(**dict(row))

    async def get_movie_crew(self, movie_id: int, crew_id: int, gender: int, name: str) -> MovieCrew | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_crew where '
                                            'movie_id=$1 and crew_id=$2 and gender=$3 and name=$4',
                                            movie_id, crew_id, gender, name)
        return MovieCrew(**dict(row)) if row else None

    async def upsert_movie_crews(self, movie_crew: MovieCrew) -> MovieCrew:
        mc = movie_crew
        if await self.get_movie_crew(mc.movie_id, mc.crew_id, mc.gender, mc.name) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into movie_crew(movie_id, crew_id, credit_id, "
                                                "department, job, gender, name) VALUES "
                                                "($1,$2,$3,$4,$5,$6,$7) returning *",
                                                mc.movie_id, mc.crew_id, mc.credit_id, mc.department,
                                                mc.job, mc.gender, mc.name)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update movie_crew set credit_id=$3, job=$5,
                        department=$4 where movie_id=$1 and crew_id=$2 and gender=$6 and name=$7 returning *""",
                                                mc.movie_id, mc.crew_id, mc.credit_id, mc.department,
                                                mc.job, mc.gender, mc.name)


        return MovieCrew(**dict(row))

    async def get_keywords(self, offset=0, limit=500) -> list[Keyword]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from keywords order by name offset $1 limit $2', offset, limit)
        return [Keyword(**dict(r)) for r in rows]

    async def get_keyword(self, keyword_id: int) -> Keyword | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from keywords where keyword_id=$1', keyword_id)
        return Keyword(**dict(row)) if row else None

    async def upsert_keyword(self, keyword: Keyword) -> Keyword:
        if keyword.keyword_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into keywords(name) VALUES ($1) returning *",
                                                keyword.name)
        elif await self.get_keyword(keyword.keyword_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into keywords(keyword_id, name) VALUES ($1,$2) returning *",
                                                keyword.keyword_id, keyword.name)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update keywords set name=$2 where keyword_id=$1 returning *""",
                                                keyword.keyword_id, keyword.name)

        return Keyword(**dict(row))

    async def get_moviekeyword(self, movie_id: int, keyword_id: int) -> MovieKeyword | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_keywords where movie_id=$1 and keyword_id=$2',
                                            movie_id, keyword_id)
        return MovieKeyword(**dict(row)) if row else None

    async def upsert_moviekeyword(self, movie_keyword: MovieKeyword) -> MovieKeyword:
        mk = movie_keyword
        if await self.get_moviekeyword(mk.movie_id, mk.keyword_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into movie_keywords(movie_id, keyword_id) VALUES "
                                                "($1,$2) returning *",
                                                mk.movie_id, mk.keyword_id)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update movie_keywords set keyword_id=$2 where movie_id=$1 
                returning *""", mk.movie_id, mk.keyword_id)

        return MovieKeyword(**dict(row))

    async def get_language(self, lang_id: int) -> Language | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from languages '
                                            'where lang_id=$1', lang_id)
        result = Language(**dict(row)) if row else None


    async def get_languages(self, offset=0, limit=100) -> list[Language]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from languages '
                                          'order by lang_id offset $1 limit $2',
                                          offset, limit)
        return [Language(**dict(row)) for row in rows]

    async def upsert_language(self, language: Language) -> Language:
        l = language
        if await self.get_language(l.lang_id) is None:
            #insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('insert into languages(lang_id, lang) values ($1, $2)'
                                                'returning *', l.lang_id, l.lang)
        else:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('update languages set lang=$2 where lang_id=$1 returning *',
                                                l.lang_id, l.lang)
        return Language(**dict(row))

    async def get_movie_language(self, movie_id: int) -> MovieLanguage:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_languages '
                                            'where movie_id=$1', movie_id)
        result = MovieLanguage(**dict(row)) if row else None
        print(result)

    async def upsert_movie_language(self, movie_lang: MovieLanguage) -> MovieLanguage:
        ml = movie_lang
        if await self.get_movie_language(ml.movie_id) is None:
            #insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('insert into movie_languages(movie_id, lang_id) values ($1, $2)'
                                                'returning *', ml.movie_id, ml.lang_id)
        else:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('update movie_languages set lang_id=$2 where movie_id=$1 '
                                                'returning *', ml.movie_id, ml.lang_id)
        return MovieLanguage(**dict(row))

    async def get_prod_company(self, comp_id: int) -> Company | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from prod_companies where company_id=$1',
                                            comp_id)

            return Pcompany(**(row)) if row else None

    async def get_prod_companies(self, offset=0, limit=100) -> list[Company]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetchrow('select * from prod_companies '
                                             'order by company_id offset $1 limit $2',
                                             offset, limit)

        return [Pcompany(**dict(row)) for row in rows]

    async def upsert_prod_company(self, company: Company) -> Company:
        c = company
        if await self.get_prod_company(c.id) is None:
            #insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('insert into prod_companies(company_id, name) values ($1, $2)'
                                                'returning *', c.id, c.name)
        else:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('update prod_companies set name=$2 where company_id=$1 returning *',
                                                c.id, c.name)
        return Pcompany(**dict(row))

    async def get_movie_company(self, movie_id: int) -> MovieCompany:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_prod_companies where movie_id=$1',
                                            movie_id)

        return MovieCompany(**dict(row)) if row else None

    async def upsert_movie_company(self, movie_comp: MovieCompany) -> MovieCompany:
        mc = movie_comp
        if await self.get_movie_company(mc.movie_id) is None:
            #insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('insert into movie_prod_companies(movie_id, company_id) values ($1, $2)'
                                                'returning *', mc.movie_id, mc.company_id)
        else:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('update movie_prod_companies set company_id=$2 where movie_id=$1 '
                                                'returning *', mc.movie_id, mc.company_id)

        return MovieCompany(**dict(row))