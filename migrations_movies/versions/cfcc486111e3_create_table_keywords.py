"""

create table keywords

Revision ID: cfcc486111e3
Creation date: 2023-05-03 09:16:22.589276

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'cfcc486111e3'
down_revision = 'f01147f524ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        f"""--sql
        CREATE TABLE keywords(
        keyword_id INT PRIMARY KEY,
        name TEXT
        );
        """
    )


def downgrade() -> None:
    op.execute(
        f"""--sql
        DROP TABLE IF EXISTS keywords CASCADE;
        """
    )