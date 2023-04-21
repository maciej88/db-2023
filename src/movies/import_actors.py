import os
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
from psycopg2 import extras
import json
from src.movies.model import CastEntry

dotenv_path = Path('../.env')
load_dotenv()
conn = psycopg2.connect(
    database=os.getenv("DATABASE"),
    user="postgres",
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    port=os.getenv("PORT"))

df = pd.read_csv("./data/tmdb_5000_credits.csv")

casts = [x for x in df['cast']]

data = set()

for i, n in enumerate(casts):
    w = json.loads(n)
    for j in w:
        a, b = (j['id'], j['name'])
        data.add((a, b))

data_for_db = data

query = """
---sql
    INSERT INTO s3878movie.actors (actor_id, name) VALUES %s
"""

extras.execute_values(
    cur=conn.cursor(),
    sql=query,
    argslist=data,
    template=None,
    page_size=100
)

conn.commit()
conn.close()