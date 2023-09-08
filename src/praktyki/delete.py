"""dry function for copy & paste to db.py"""


async def wipe_data(self, uid: uuid):
    query = """
           DELETE FROM persons WHERE person_id != $1
       """
    async with self.pool.acquire() as connection:
        await connection.execute(query, uid)
        print(f'Data wiped from database, saved: {uid}')