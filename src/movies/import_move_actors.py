import os
import json
import pandas as pd
from pandas import json_normalize
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
from psycopg2 import extras

dotenv_path = Path('../.env')
load_dotenv()
conn = psycopg2.connect(
    database=os.getenv("DATABASE"),
    user="postgres",
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    port=os.getenv("PORT"))

df = pd.read_csv("data/tmdb_5000_credits.csv")

# able1_df = pd.read_sql_query("SELECT movie_id FROM s3878movie.movies", conn)
# table2_df = pd.read_sql_query("SELECT actor_id FROM s3878movie.actors", conn)
# df = pd.DataFrame(data)

casts = [x for x in df['cast']]


data = set()

df = pd.DataFrame(
    columns=['cast_id', 'character', 'credit_id', 'gender', 'id_cast', 'name', 'order'])

for i, n in enumerate(casts):
    w = json.loads(n)
    for j in w:
        cast_id = j['cast_id']
        character = j['character']
        credit_id = j['credit_id']
        gender = j['gender']
        id_cast = j['id']
        name = j['name']
        order = j['order']


# casts = [x for x in df['cast']]
#
# data = set()
#
# for i, n in enumerate(casts):
#     w = json.loads(n)
#     for j in w:
#         a, b = (j['id'], j['name'])
#         data.add((a, b))
#
# data_for_db = data


# query = """
# ---sql
#     INSERT INTO s3878movie.movies (movie_id, title) VALUES %s
# """
#
# extras.execute_values(
#     cur=conn.cursor(),
#     sql=query,
#     argslist=data,
#     template=None,
#     page_size=100
# )
#
# conn.commit()
# conn.close()