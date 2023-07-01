"""

create db voting

Revision ID: 0dcc258a81bc
Creation date: 2023-06-30 16:38:18.703577

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '0dcc258a81bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    create table users(
    user_id uuid DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
    name text not null
);
create table elections(
    election_id uuid DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
    name text not null unique
);

create table participation(
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    election_id UUID NOT NULL REFERENCES elections(election_id) ON DELETE CASCADE
);

create table tokens(
    election_id UUID NOT NULL REFERENCES elections(election_id) ON DELETE CASCADE,
    token_id uuid DEFAULT GEN_RANDOM_UUID() PRIMARY KEY
);

create table votes(
    election_id UUID NOT NULL REFERENCES elections(election_id) ON DELETE CASCADE,
    votevalue int NOT NULL
);
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE users,
    DROP TABLE elections,
    DROP TABLE participation,
    DROP TABLE tokens,
    DROP TABLE votes,
    """)
