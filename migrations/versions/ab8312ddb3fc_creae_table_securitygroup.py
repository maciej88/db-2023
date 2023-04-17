"""

creae table securitygroup

Revision ID: ab8312ddb3fc
Creation date: 2023-03-25 11:26:22.490558

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'ab8312ddb3fc'
down_revision = '7f4f938e69ba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f"""
    create table securitygroup
(
    groupid   uuid default gen_random_uuid() primary key not null,
    groupname text
)
    """)


def downgrade() -> None:
    op.execute(f"""
    --sql
    drop table if exists securitygroup cascade
    """)
