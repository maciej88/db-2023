import os
import pandas as pd
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

data = pd.read_csv("./data/tmdb_5000_movies.csv")

# df = pd.DataFrame(data)

df = data[['id','title']]

def row_to_tuple(row):
    return (row['id'], row['title'])

data = df.apply(row_to_tuple, axis=1).tolist()

query = """
---sql
    INSERT INTO s3878movie.movies (movie_id, title) VALUES %s
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