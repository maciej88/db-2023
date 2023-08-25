import unittest
from asyncio import gather
from unittest import IsolatedAsyncioTestCase
from db import *


class Test(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        print('setup')
        self.db = DbService()
        self.uid1 = uuid4()
        self.eid1 = uuid4()

        await self.db.initialize()

    async def asyncTearDown(self):
        print('teardown')

    async def test_can_create_user(self):
        user = await self.db.create_user(User(self.uid1, 'xi'))
        await self.db.delete_user(user.uid)

    # todo: dodać test tworzący i usuwający election

    # todo:  dodać test w którym user z uid1 rejestruje się do wyborów eid1, czyli test do db.register_for_election

    async def test_cannot_get_many_tokens_for_user(self):
        tasks = []
        N = 30
        errors = 0
        for i in range(N):
            tasks.append(create_task(self.db.register_for_election(self.eid1, self.uid1)))

        tokens = set()
        for t in tasks:
            try:
                # no error
                g = await t
                tokens.add(g)
            except VotingError as e:
                # error
                errors += 1

        self.assertEquals(errors, N - 1)
        self.assertEquals(len(tokens), 1)

    async def test_token_can_vote_exactly_once(self):
        N = 30

        token = await self.db.register_for_election(self.eid1, self.uid1)

        tasks = []
        for i in range(N):
            tasks.append(create_task(self.db.vote(token, 3)))

        errors = 0
        for t in tasks:
            try:
                # no error
                g = await t
            except VotingError as e:
                # error
                errors += 1

        self.assertEquals(errors, N - 1)

        # assert exactly one vote in table votes
        # assert len(self.db.get_votes_by_eid(self.eid1)) == 1


if __name__ == "__main__":
    unittest.main()
