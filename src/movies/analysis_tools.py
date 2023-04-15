import json
from collections import defaultdict

import pandas as pd

from movies.model import CastEntry

pd.options.display.max_rows = 10


def get_cast_of_movie(index: int, cast_field: str) -> list[CastEntry]:
    dicts = json.loads(cast_field)
    entries = []
    for d in dicts:
        entry = CastEntry(movie_index=index, **d)
        entries.append(entry)
    return entries


def check_unique_cast_creditid(casts: list[str]):
    credit_ids = []
    for i, movie in enumerate(casts):
        entries = get_cast_of_movie(i, movie)
        credit_ids.extend([c.credit_id for c in entries])

    unique = (len(credit_ids) == len(set(credit_ids)))
    print(f'{unique=}')


def check_assignment_actor_actorid(casts: list[str]):
    name_id_pairs = []
    for i, movie in enumerate(casts):
        entries = get_cast_of_movie(i, movie)
        for e in entries:
            print(e)
        name_id_pairs.extend([(c.id, c.name) for c in entries])

    unique_pairs = set(name_id_pairs)
    n_pairs = len(unique_pairs)
    n_names = len(set([c for i, c in unique_pairs]))  # unique names
    n_ids = len(set([i for i, c in unique_pairs]))  # unique id's

    print(f'{n_pairs=}')
    print(f'{n_ids=}')
    print(f'{n_names=}')


def find_duplicates(casts: list[str]):
    name_id_pairs = []
    for i, movie in enumerate(casts):
        entries = get_cast_of_movie(i, movie)
        name_id_pairs.extend([(c.id, c.name) for c in entries])

    unique_pairs = set(name_id_pairs)
    id_to_name = defaultdict(lambda : set())
    for (id,name) in unique_pairs:
        id_to_name[id].add(name)

    for (k,v) in id_to_name.items():
        if len(v) > 1:
            print('id->names ', k, v)

    # -----
    name_to_id = defaultdict(lambda : set())
    for (id,name) in unique_pairs:
        name_to_id[name].add(id)

    for (k,v) in name_to_id.items():
        if len(v) > 4:
            print('name->ids ', k, v)

if __name__ == '__main__':
    df = pd.read_csv('data/tmdb_5000_credits.csv')
    casts_ = list(df['cast'])  # list[str]
    # check_unique_cast_creditid(casts_)
    check_assignment_actor_actorid(casts_)
    # find_duplicates(casts_)
