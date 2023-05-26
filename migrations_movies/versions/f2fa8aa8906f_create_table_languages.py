"""

create table languages

Revision ID: f2fa8aa8906f
Creation date: 2023-05-03 09:24:38.561081

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'f2fa8aa8906f'
down_revision = '4573c47e2a60'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f"""
    --sql 
    CREATE TABLE languages (
        lang_id VARCHAR(2) UNIQUE PRIMARY KEY,
        lang TEXT NOT NULL
    )
""")


def downgrade() -> None:
    op.execute(f"""
    DROP TABLE IF EXISTS languages CASCADE;
""")
