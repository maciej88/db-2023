import asyncio
import uuid
from asyncio import run, create_task
from datetime import datetime
from os import getenv
from random import choice
import uuid

import asyncpg
from dotenv import load_dotenv

from model import *

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')




class DbService:

    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5,
                                              server_settings={'search_path': SCHEMA})

        print(f'connected to [{URL}]')

    async def create_user(self, user: User) -> User:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(
                """insert into Users(user_id, name) 
                    VALUES ($1,$2) returning *""", user.user_id, user.name)
        return User(**dict(row))

    async def delete_user(self, uid: uuid):
        async with self.pool.acquire() as connection:
            deleted = await connection.fetch("""SELECT * FROM Users WHERE user_id=$1""", uid)
            await connection.execute("""DELETE FROM Users WHERE user_id=$1""", uid)
        return print(f"Deleted {[User(**dict(d)) for d in deleted]}")

    async def create_election(self, election: Election) -> Election:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(
                """insert into Elections(election_id, name) 
                    VALUES ($1,$2) returning *""", election.election_id, election.name)
        return Election(**dict(row))

    async def delete_election(self, eid: uuid):
        async with self.pool.acquire() as connection:
            deleted = await connection.fetch("""SELECT * FROM Elections WHERE election_id=$1""", eid)
            await connection.execute("""DELETE * FROM Elections WHERE election_id=$1""", eid)
        return print(f"Deleted {[Election(**dict(d)) for d in deleted]}")


    async def register_for_election(self, eid: uuid, uid: uuid) -> uuid:
        """
        User with `uid` registers for election `eid`; raises VotingError if already voted, or
        `uid` or `eid` are invalid.

        Transactional.

        :param eid:
        :param uid:
        :return:
        """

    async def vote(self, tokenid: uuid, votevalue: int) -> uuid:
        """
        User with token `tokenid` votes in election. Appropriate row is created in Votes; token is removed.


        Transactional.

        :param eid:
        :param uid:
        :raises: VotingError if tokenid is invalid
        :return:
        """


def ts():
    return datetime.now().timestamp()


async def main():
    db = DbService()
    await db.initialize()

    e = Election(election_id=uuid.uuid1(), name='Li')
    e_ = await db.create_election(e)
    print(e_)
    # d = User(user_id='c72529f0-175b-11ee-b229-695f43ebc72c')
    # d_ = await db.delete_user('c72529f0-175b-11ee-b229-695f43ebc72c')
    # print(d_)


if __name__ == '__main__':
    run(main())

