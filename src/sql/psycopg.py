import os

import pandas as pd
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import pandas

dotenv_path = Path('./.env')
load_dotenv()

conn=psycopg2.connect(
    database=os.getenv("DATABASE"),
    user="postgres",
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    port=os.getenv("PORT"),
    options=f"-c search_path={os.getenv('SCHEMA')}")

# cur = conn.cursor()
query = "SELECT * FROM movie_crew"
# cur.execute(query)

# rows = cur.fetchall()
#
# for row in rows:
#     print(row)

# conn.commit()
# cur.close()
df = pd.read_sql(query, conn)

conn.close()

print(df)