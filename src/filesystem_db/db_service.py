from __future__ import annotations

import asyncio
from asyncio import run, sleep
from uuid import uuid4

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

    # files

    async def get_files(self, offset=0, limit=500) -> list[File]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch("""select * from files 
            order by file_id offset $1 limit $2""", offset, limit)
        return [File(**dict(r)) for r in rows]

    async def get_file(self, file_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from files where file_id=$1', file_id)
        return File(**dict(row)) if row else None

    async def upsert_file(self, file: File) -> File:
        f = file  # alias

        if file.file_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into files(name, bytes, depth, accessed, modified, basename, extension,
                        type, mode, parent_path, full_path) 
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) returning *""",
                    f.name, f.bytes, f.depth, f.accessed, f.modified, f.basename, f.extension,
                    f.type, f.mode, f.parent_path, f.full_path)
                return File(**dict(row))

        elif await self.get_file(file.file_id) is None:
            # file_id present in `file`, but no such row in DB

            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into files(file_id, name, bytes, depth, accessed, modified, basename, extension,
                        type, mode, parent_path, full_path) 
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12) returning *""",
                    f.file_id, f.name, f.bytes, f.depth, f.accessed, f.modified, f.basename, f.extension,
                    f.type, f.mode, f.parent_path, f.full_path)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""
                    update files set name=$2, bytes=$3, depth=$4, accessed=$5, modified=$6, basename=$7, extension=$8,
                        type=$9, mode=$10, parent_path=$11, full_path=$12
                        where file_id=$1 returning *""",
                                                f.file_id, f.name, f.bytes, f.depth, f.accessed, f.modified, f.basename,
                                                f.extension,
                                                f.type, f.mode, f.parent_path, f.full_path)

        return File(**dict(row))

    async def delete_file(self, file_id: int):
        async with self.pool.acquire() as connection:
            await connection.execute('DELETE from files where file_id=$1', file_id)
        return print(f"Deleted by id: {file_id}")


    async def heal_file_id(self):
        async with self.pool.acquire() as connection:
            await connection.execute("SELECT setval('files_file_id_seq',(SELECT MAX(file_id) FROM files));")


if __name__ == '__main__':
    async def try_it():
        db = DbService()
        await db.initialize()
        await db.delete_file(1)
        # now = datetime.now()
        #
        # f = File(file_id=10 + 10 ** 6, name='gs', bytes=10, depth=2, accessed=now, modified=now,
        #          basename='gs', extension='', type='f', mode='-rwxrwxrwx', parent_path='/', full_path='/gs')
        # f_ = await db.upsert_file(f)
        # await db.heal_file_id()
        # print(f_)


    asyncio.run(try_it())
