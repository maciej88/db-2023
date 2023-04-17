"""

creae table accesskey

Revision ID: 7f4f938e69ba
Creation date: 2023-03-25 11:17:50.921601

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '7f4f938e69ba'
down_revision = 'e120aeca0fb1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    --sql
    create table accesskey
(
    keyid uuid DEFAULT gen_random_uuid() primary key,
    name  text not null UNIQUE
);
    """)


def downgrade() -> None:
    op.execute(
        f"""--sql
    drop table if exists accesskey cascade
    """)
