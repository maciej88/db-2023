from asyncio import run, sleep

import asyncpg
from dotenv import load_dotenv
from os import getenv

import pandas as pd

import json

from db_service import DbService

from model import Movie
from src.movies.analysis_tools import *


async def main():
    db = DbService()
    await db.initialize()  # tu łączymy się z bazą danych

    actors = get_movie_actors('data/tmdb_5000_credits.csv')

    print(f'all actors: {len(actors)}')

    for i, actor in enumerate(actors):
        await db.upsert_movieactor(actor)
        if i % 100 == 0:
            print(f'import in {i / len(actors) * 100:.1f}% done')

    await sleep(1)


if __name__ == '__main__':
    run(main())
