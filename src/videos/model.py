from uuid import uuid4
import uuid
from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    user_id: uuid
    name: str


@dataclass
class Video:
    video_id: uuid
    title: str
    file_name: str
    description: str
    created: datetime
    edited: datetime
    owner: uuid


@dataclass
class Comment:
    comment_id: uuid
    author: uuid
    content: str
    created: datetime
    edited: datetime


@dataclass
class VideoLike:
    like_id: uuid
    video_id: uuid
    user_id: uuid
    like_level: int

    def __post_init__(self):
        # validate like:
        if not (self.like_level == 0 or self.like_level == -1 or self.like_level == 1):
            raise ValueError("like out of range")
