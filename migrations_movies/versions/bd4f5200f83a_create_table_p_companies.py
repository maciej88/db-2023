"""

create table p_companies

Revision ID: bd4f5200f83a
Creation date: 2023-05-03 10:24:16.780081

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'bd4f5200f83a'
down_revision = '9a5bd69dadde'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f"""
    --sql
    CREATE TABLE prod_companies(
        company_id SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name TEXT NOT NULL
        );
""")


def downgrade() -> None:
    op.execute(f"""
    DROP TABLE IF EXISTS prod_companies CASCADE;
""")
