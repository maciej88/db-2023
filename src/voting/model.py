from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class User:
    user_id: UUID
    name: str


@dataclass
class Election:
    election_id: UUID
    name: str


@dataclass
class Token:
    election_id: UUID
    token_id: UUID


@dataclass
class Vote:
    election_id: UUID
    votevalue: int


@dataclass
class Participation:
    uid: UUID
    eid: UUID


class VotingError(RuntimeError):
    pass


if __name__ == '__main__':
    try:
        raise VotingError('ha ha ha')
    except RuntimeError as e:
        print(e)
