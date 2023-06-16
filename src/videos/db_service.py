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

    async def get_videos(self, offset=0, limit=500) -> list[Video]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch("""select * from videos 
            order by video_id offset $1 limit $2""", offset, limit)
        return [Video(**dict(r)) for r in rows]

    async def get_likes(self, offset=0, limit=500) -> list[VideoLike]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch("""select * from videolikes
            order by like_id offset $1 limit $2""", offset, limit)
        return [VideoLike(**dict(r)) for r in rows]

    async def get_like(self, like_id: str) -> VideoLike:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from videolikes where like_id=$1', like_id)
        return VideoLike(**dict(row)) if row else None

    async def get_comments(self, offset=0, limit=500) -> list[Comment]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch("""select * from comments
            order by comment_id offset $1 limit $2""", offset, limit)
        return [Comment(**dict(r)) for r in rows]

    async def get_comment(self, comment_id: str) -> Comment:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from comments where comment_id=$1', comment_id)
        return Comment(**dict(row)) if row else None

    async def set_like(self, like: VideoLike) -> VideoLike:
        if like.like_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into videolikes(video_id, user_id, like_level) 
                        VALUES ($1,$2,$3) returning *""",
                    like.video_id, like.user_id, like.like_level)
        elif await self.get_like(like.like_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into videolikes(like_id, video_id, user_id, like_level) 
                        VALUES ($1,$2,$3,$4) returning *""",
                    like.like_id, like.video_id, like.user_id, like.like_level)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update videolikes set video_id=$2, user_id = $3,
                                                like_level = $4
                                                where like_id=$1 returning *""",
                                                like.like_id, like.video_id, like.user_id, like.like_level)

        return VideoLike(**dict(row))


    async def post_comment(self, comment: Comment) -> Comment:
        if comment.comment_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into comments(author, content, created, edited) 
                        VALUES ($1,$2,$3,$4) returning *""",
                    comment.author, comment.content, comment.created, comment.edited)
        elif await self.get_comment(comment.comment_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into comments(comment_id, author, content, created, edited) 
                        VALUES ($1,$2,$3,$4,$5) returning *""",
                    comment.comment_id, comment.author, comment.content, comment.created, comment.edited)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update comments set author=$2, contend = $3,
                                                    created = $4, edited = $5
                                                    where comment_id=$1 returning *""",
                                                comment.comment_id, comment.author, comment.content,
                                                comment.created, comment.edited)

        return Comment(**dict(row))


if __name__ == '__main__':

    new_uuid = uuid.uuid4()
    print(new_uuid)
    # 'ca9b56f7-7ebe-4901-ba66-b462a99a81ba'
    async def try_it():
        db = DbService()
        await db.initialize()
        # v_ = await db.get_videos()
        # print(v_)
        now = datetime.now()
        # like = VideoLike(like_id=new_uuid,
        #                  video_id='5ca409a1-f364-4a7f-8caf-22df89d3c8fe',
        #                  user_id='f9757f80-d726-4fcc-8933-6ef8f2ca26fe', like_level=5)
        # l_ = await db.set_like(like)
        # print(l_)
        comment = Comment(comment_id=new_uuid, author='f9757f80-d726-4fcc-8933-6ef8f2ca26fe', content='some text', created=now,
                          edited=now)
        c_ = await db.post_comment(comment)
        print(c_)

    asyncio.run(try_it())
