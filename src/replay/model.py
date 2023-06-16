from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class Channel:
    channel_id: UUID
    username: str


@dataclass
class Video:
    video_id: UUID
    title: str
    owner: UUID
    filename: str
    description: str
    created: datetime
    edited: datetime


@dataclass
class Comment:
    comment_id: UUID
    author: UUID
    content: str
    video_id: UUID
    parent_comment: UUID | None
    created: datetime
    edited: datetime


@dataclass
class Playlist:
    playlist_id: UUID
    playlist_name: str
    playlist_owner: UUID
    created: datetime
    edited: datetime

@dataclass
class VideoLike:
    video_id: UUID
    channel_id: UUID
    is_like: bool

class ReplayException(RuntimeError):
    pass
