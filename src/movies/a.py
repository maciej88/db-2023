import json

import pandas as pd

from movies.model import CastEntry

pd.options.display.max_rows = 10

df = pd.read_csv('data/tmdb_5000_credits.csv')

# print(df.head(0))
# print(df['cast'])
# print(type(df['cast']))

casts = [x for x in df['cast']]  # lista wartości w kolumnie 'casts'
# print(casts[0])
print(type(casts[0]))  # str
w = json.loads(casts[0])    # list[dict]

for cs in w:
    print(cs)
    cast = CastEntry(movie_index=0, **cs)
    print(cast.name, cast.id)

# 2 pytania:
# 1) czy pole "id" jest unikalne dla danego aktora, czyli pola "name" (czyli: czy można interpretować "id" jako "actor_id")
# 2) czy pole "credit_id" jest unikalne wśród wszystkich filmów i elementów listy cast każdego z filmów...
#  (czyli: czy możnaby go w zasadzie traktować jako primary key w tabeli "Cast" którą będziemy tworzyli)
