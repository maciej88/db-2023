"""

create table movie_keywords

Revision ID: 4573c47e2a60
Creation date: 2023-05-03 09:16:47.459651

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '4573c47e2a60'
down_revision = 'cfcc486111e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        f"""--sql
        CREATE TABLE movie_keywords(
        movie_id INT REFERENCES movies(movie_id) ON DELETE CASCADE,
        keyword_id INT REFERENCES keywords(keyword_id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    op.execute(
        f"""--sql
        DROP TABLE IF EXISTS movie_keywords CASCADE;
        """
    )
