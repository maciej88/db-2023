import asyncio
import uuid
from asyncio import run, create_task
from datetime import datetime
from os import getenv
from random import choice

import asyncpg
from dotenv import load_dotenv

from model import *

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')

new_token = uuid4()


# UUID validator:
def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


class DbService:

    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5,
                                              server_settings={'search_path': SCHEMA})

        print(f'connected to [{URL}]')

    async def create_user(self, user: User) -> User:
        query = """
               INSERT INTO users (uid, name) VALUES ($1, $2) RETURNING *
           """
        values = (user.uid, user.name)
        async with self.pool.acquire() as connection:
            result = await connection.fetchrow(query, *values)
        res = User(*result)
        print(f'Created election: {res}')
        return res

    async def delete_user(self, uid: uuid):
        query = """
               DELETE FROM users WHERE uid = $1
           """
        async with self.pool.acquire() as connection:
            await connection.execute(query, uid)
            print(f'Removed user {uid}')

    async def create_election(self, election: Election) -> Election:
        query = """
               INSERT INTO elections (eid, name) VALUES ($1, $2) RETURNING *
           """
        values = (election.eid, election.name)
        async with self.pool.acquire() as connection:
            result = await connection.fetchrow(query, *values)
        res = Election(*result)
        print(f'Created election: {res}')
        return res

    async def delete_election(self, eid: uuid):
        query = """
               DELETE FROM elections WHERE eid = $1
           """
        async with self.pool.acquire() as connection:
            await connection.execute(query, eid)
            print(f'Removed election {eid}')

    async def register_for_election(self, uid: uuid, eid: uuid) -> uuid:
        """
        User with `uid` registers for election `eid`; raises VotingError if already voted, or
        `uid` or `eid` are invalid.

        Transactional.

        :param eid: given by user (id for election)
        :param uid: given by user (from table users - as outside base)
        :return:
        """
        query0 = """
                SELECT * FROM participation WHERE uid = $1;
                """
        query1 = """
                begin transaction;
                """

        query2 = """
                INSERT INTO participation (uid, eid) VALUES ($1, $2) RETURNING *;
                """

        query3 = """
                INSERT INTO tokens (eid, tokenid) VALUES ($1, $2)
                ON CONFLICT (tokenid) DO NOTHING;
                """

        query4 = """
                COMMIT;
                """

        async with self.pool.acquire() as connection:
            # Checking if already voted
            votes_table = await connection.execute(query0, uid)
            if int(votes_table[-1]) > 0:
                raise VotingError('User has already voted.')

            await connection.execute(query1)

            # Check if the `uid` or `eid` are valid.
            if not is_valid_uuid(eid) or not is_valid_uuid(uid):
                raise VotingError('Invalid uid or eid.')

            await connection.execute(query2, uid, eid)
            await connection.execute(query3, eid, new_token)
            await connection.execute(query4)
            res = new_token
            print(f'token for voting: {new_token}')
            return res

    async def vote(self, tokenid: uuid, votevalue: int) -> uuid:
        """
        User with token `tokenid` votes in election. Appropriate row is created in Votes; token is removed.


        Transactional.

        :param eid: taken from tokens table via tokenid
        :param tokenid: given by user
        :param votevalue: given by user
        :raises: VotingError if tokenid is invalid
        :return:
        """
        query0 = """
            begin transaction;
            """
        query1 = """
            SELECT * FROM tokens WHERE tokenid = $1;
            """
        query2 = """
            SELECT eid FROM tokens WHERE tokenid = $1;
            """
        query3 = """
            INSERT INTO votes (eid, votevalue) VALUES ($1, $2) RETURNING *;
            """
        query4 = """
            DELETE FROM tokens WHERE tokenid = $1;
            """
        query5 = """
            COMMIT;
            """
        async with self.pool.acquire() as connection:
            votes_table = await connection.execute(query1, tokenid)
            # token validation:
            if not int(votes_table[-1]) == 1 and not is_valid_uuid(tokenid):
                raise VotingError('You going to prison!')
            await connection.execute(query0)
            eid = await connection.fetchval(query2, tokenid)
            eid = str(eid)
            print(eid)
            print(votevalue)
            values = (eid, votevalue)
            print(*values)
            result = await connection.fetchrow(query3, *values)
            await connection.execute(query4, tokenid)
            await connection.execute(query5)
            print(f"You voted in {eid} as {votevalue}")
            res = Vote(*result)
            return res

    async def create_token(self, token: Token) -> Token:
        query = """
                INSERT INTO tokens (eid, tokenid) VALUES ($1, $2) RETURNING *;
                """
        values = (token.eid, token.tokenid)
        async with self.pool.acquire() as connection:
            result = await connection.fetchrow(query, *values)
        res = Token(*result)
        print(f'Created token: {res}')
        return res


def ts():
    return datetime.now().timestamp()


async def main():
    db = DbService()
    await db.initialize()
    # new_uid = uuid4()
    # await db.create_user(User(new_uid, 'bob'))
    # await db.delete_user(user.uid)
    # await db.register_for_election(
    #     uid='8f8a5b72-372f-46d6-99cb-091ae48cfc9c', eid='aff5b974-70fb-43d7-afe2-a9ed53048082')
    # await db.delete_election(elect.eid)
    # await db.vote(tokenid='299c1d2c-1e03-4262-8360-fc6bcf29f99e', votevalue=1)
    await db.create_token(Token(
        eid='aff5b974-70fb-43d7-afe2-a9ed53048082', tokenid='299c1d2c-1e03-4262-8360-fc6bcf29f99e'))


if __name__ == '__main__':
    run(main())
