import uuid
from asyncio import run
from datetime import datetime
from os import getenv
from uuid import uuid4

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

    async def get_all_votes(self, eid: uuid) -> list[Vote]:
        async with self.pool.acquire() as c:
            votes = await c.fetch('select * from votes where eid=$1 order by votevalue', eid)
            votes = [Vote(*t) for t in votes]
            return votes

    async def register_for_election(self, eid: uuid, uid: uuid) -> Token:
        """
        User with `uid` registers for election `eid`; raises VotingError if already voted, or
        `uid` or `eid` are invalid.

        Transactional.

        :param eid:
        :param uid:
        :return: token for the election
        """

        async with self.pool.acquire() as con:
            try:
                async with con.transaction(isolation='serializable') as tx:
                    # create new token
                    res = await con.fetchrow('insert into tokens(eid) values ($1) returning *', eid)
                    token = Token(*res)
                    await con.execute('insert into participation(eid,uid) values ($1,$2)', eid, uid)
                print(f'generated token: {str(token.tokenid)[:6]}...')
                return token

            except asyncpg.exceptions.SerializationError as f:
                print(f'serialization error for {eid=}, {uid=}')

            except asyncpg.exceptions.UniqueViolationError as f:
                print('repeated key')
                raise VotingError(f'repeated registration for {uid=}, {eid=}')

            except RuntimeError as e:
                print(f'runtime error error for {eid=}, {uid=}')

    async def goo(self):
        async with self.pool.acquire() as c:
            res = await c.fetchrow("select * from users where name like 'X%' order by name")
            print(res)
            print(type(res))
        if res:
            print('znaleziono wyniki')
        else:
            print('nie ma wyników')


    async def vote(self, tokenid: uuid, votevalue: int) -> uuid:
        """
        User with token `tokenid` votes in election. Appropriate row is created in Votes; token is removed.


        Transactional.

        :param eid:
        :param uid:
        :raises: VotingError if tokenid is invalid
        :return:
        """
        async with self.pool.acquire() as con:
            try:
                async with con.transaction(isolation='serializable') as tx:
                    # create new token
                    res = await con.fetchrow('select * from tokens where tokenid=$1', tokenid)
                    if res is None:
                        raise VotingError('invalid token')

                    token = Token(*res)
                    await con.execute('delete from tokens where tokenid=$1', tokenid)

                    await con.execute('insert into votes(eid, votevalue) values ($1,$2)', token.eid, votevalue)

                print(f'token {str(token.tokenid)}... voted in election: {token.eid}')
                return tokenid

            except asyncpg.exceptions.SerializationError as f:
                print(f'serialization error for {tokenid=}')
                raise VotingError(f'concurrent acces for {tokenid=}')

            except RuntimeError as e:
                print(f'runtime error for {tokenid=}, error: {e}')
                raise VotingError(f'error voting with {tokenid=}, e')

    async def test_cleanup(self):
        """
        Test-only method.
        """
        query = """
               DELETE FROM elections WHERE true;
               DELETE FROM users WHERE true;
           """
        async with self.pool.acquire() as connection:
            await connection.execute(query)
            print(f'Removed all users and elections')

    async def test_get_all_tokens(self):
        """
        Test-only method.
        """
        async with self.pool.acquire() as c:
            tokens = await c.fetch('select * from tokens order by eid,tokenid')
            tokens = [Token(*t) for t in tokens]
            return tokens


def ts():
    return datetime.now().timestamp()


async def main():
    db = DbService()
    await db.initialize()
    # uid = uuid4()
    # user = await db.create_user(User(uid, 'xi'))
    # await db.delete_user(user.uid)
    #
    # elect = await db.create_election(Election(uid, 'Wybory normalne'))
    # await db.delete_election(elect.eid)
    await db.goo()

    pass


if __name__ == '__main__':
    run(main())
