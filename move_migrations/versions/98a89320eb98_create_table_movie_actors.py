"""

create table move_actors

Revision ID: 98a89320eb98
Creation date: 2023-04-17 21:34:52.177630

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '98a89320eb98'
down_revision = 'bcf7c690e6dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        --sql
        create table movie_actors
    (
        credit_id text,
        movie_id  integer references s3878movie.movies (movie_id) on DELETE CASCADE,
        actor_id integer references s3878movie.actors (actor_id) on DELETE CASCADE,
        cast_id integer,
        character text,
        gender integer,
        "order" integer
    );
        """)


def downgrade() -> None:
    op.execute(
        f"""--sql
        drop table if exists movie_actors cascade
        """)
