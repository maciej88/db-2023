import json

import pandas as pd

from movies.model import *

pd.options.display.max_rows = 6

df = pd.read_csv('data/tmdb_5000_credits.csv')


crews = [x for x in df['crew']]
# print(type(crews[0]))  # str

for i, c in enumerate(crews):
    print(f'movie_position: {i}, data: {c[:60]}')

w = json.loads(crews[0])    # list[dict]
for item in w:
    print(CrewEntry(movie_index=0,**item))
