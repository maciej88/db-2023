"""

create table movies

Revision ID: fe552a3da5b7
Creation date: 2023-04-17 20:12:00.472586

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'fe552a3da5b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        --sql
        create table movies
    (
        movie_id integer unique,
        title  text
    );
        """)


def downgrade() -> None:
    op.execute(
        f"""--sql
        drop table if exists movies cascade
        """)