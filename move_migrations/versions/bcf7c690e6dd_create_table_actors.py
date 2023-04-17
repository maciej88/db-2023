"""

create table actors

Revision ID: bcf7c690e6dd
Creation date: 2023-04-17 21:25:23.425097

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'bcf7c690e6dd'
down_revision = 'fe552a3da5b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        --sql
        create table actors
    (
        actor_id integer unique,
        name  text
    );
        """)


def downgrade() -> None:
    op.execute(
        f"""--sql
        drop table if exists actors cascade
        """)
