"""

drop table secured_resource

Revision ID: f0ebaaa306b1
Creation date: 2023-03-25 11:42:55.313549

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'f0ebaaa306b1'
down_revision = 'ab8312ddb3fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f"""
        create table group_key
(
    groupid uuid references s3878a.securitygroup (groupid) on delete CASCADE,
    keyid   uuid references s3878a.accesskey (keyid) on delete CASCADE
)""")


def downgrade() -> None:
    op.execute(f"""
        --sql
        drop table if exists group_key cascade
        """)
