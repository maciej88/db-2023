from asyncio import run
import asyncpg
from dotenv import load_dotenv
from os import getenv
from model import *

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')


class DbService:

    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5,
                                              server_settings={'search_path': SCHEMA})

    async def get_videos(self, offset=0, limit=500) -> list[Video]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from video order by title offset $1 limit $2', offset, limit)
        return [Video(**dict(r)) for r in rows]

    async def is_like_set(self, video_id: UUID, channel_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            ans = await connection.fetch('select count(*) = 0 from video_likes where video_id=$1 and channel_id=$2',
                                         video_id, channel_id)
        return not ans

    async def set_like(self, video_id: UUID, channel_id: UUID, like_level: bool):
        # fixme: allows multiple likes of the same video_id by channel_id
        if await self.is_like_set(video_id, channel_id):
            async with self.pool.acquire() as connection:
                await connection.fetch('update video_likes set is_like=$1 where video_id=$2 and channel_id=$3',
                                       like_level, video_id, channel_id)
        else:
            async with self.pool.acquire() as connection:
                await connection.fetch('insert into video_likes(video_id, channel_id, is_like)'
                                       'values ($1, $2, $3) returning *', video_id, channel_id, like_level)

    async def remove_like(self, video_id: UUID, channel_id: UUID) -> None:
        async with self.pool.acquire() as connection:
            deleted = await connection.fetch("""SELECT * FROM video_likes WHERE video_id=$1 and channel_id=$2""",
                                             video_id, channel_id)
            await connection.execute("""DELETE from video_likes where video_id=$1 and channel_id=$2""",
                                     video_id, channel_id)
        return print(f"Deleted {[VideoLike(**dict(d)) for d in deleted]}")

    async def is_top_level_comment(self, parent_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            ans = await connection.fetch('select parent_comment is null from comment where comment_id = $1', parent_id)
        return ans

    async def is_spam(self, author_id: UUID, video_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            # note: fetch returns Recort<False> (not a bool); fetchval returns a bool
            ans = await connection.fetchval("""select exists (select 1 from comment where author = $1 and video_id = $2)""",
                                         author_id, video_id)

        return ans

    async def post_comment(self, author_id: UUID, content: str, video_id: UUID, parent_comment: UUID | None) -> Comment:
        if parent_comment is not None:
            if not (await self.is_top_level_comment(parent_comment)):
                raise ReplayException('Comments nesting cannot be deeper than 1 level')

        # todo: consider using unique(video_id, channel_id) constraint on video_likes table
        if not await self.is_spam(author_id, video_id):
            async with self.pool.acquire() as connection:
                new_comment = await connection.fetch('insert into comment(author, content, video_id, parent_comment) values'
                                       '($1, $2, $3, $4) returning *', author_id, content, video_id, parent_comment)
                return new_comment
        else:
            raise ReplayException('You spammer!')


async def main_():
    db = DbService()
    await db.initialize()
    videos = await db.get_videos()
    print(videos)
    video_id, user_id = UUID('771c8d3e-1c32-4a9b-9cb1-6c278b52580c'), UUID('8aa66945-77b2-4bb2-bd17-00da523c561e')
    # await db.set_like(video_id, user_id, like_level=True)
    # await db.post_comment(user_id, 'test', video_id, parent_comment=None)
    await db.remove_like(video_id=video_id, channel_id=user_id)


if __name__ == '__main__':
    run(main_())
