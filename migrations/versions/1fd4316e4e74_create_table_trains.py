"""

create table trains

Revision ID: 1fd4316e4e74
Creation date: 2023-03-24 16:35:31.958761

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '1fd4316e4e74'
down_revision = 'b527b3161830'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        f"""--sql
        CREATE TABLE trains
        (
            trainid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            active BOOL DEFAULT false
        );
        """
    )


def downgrade() -> None:
    op.execute(
        f"""--sql
        DROP TABLE trains;
        """
    )
