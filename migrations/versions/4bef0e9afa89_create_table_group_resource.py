"""

create table group_resource

Revision ID: 4bef0e9afa89
Creation date: 2023-03-27 18:12:37.620322

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '4bef0e9afa89'
down_revision = 'f0ebaaa306b1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f"""
    --sql
    create table group_resource
(
    groupid    uuid references s3878a.securitygroup (groupid) on delete CASCADE,
    resourceid uuid references s3878a.secured_resource (resource_id) on delete CASCADE
);
    """)


def downgrade() -> None:
    op.execute(f"""
    --sql
    drop table if exists group_resource cascade
    """)
