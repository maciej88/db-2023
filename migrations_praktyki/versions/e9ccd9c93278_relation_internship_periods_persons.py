"""

relation_internship_periods_persons

Revision ID: e9ccd9c93278
Creation date: 2023-09-09 12:28:57.157374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9ccd9c93278'
down_revision = 'a12914d6ed97'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE  internship_periods
        ADD CONSTRAINT internship_periods_persons
        FOREIGN KEY (student_id) REFERENCES persons ON DELETE CASCADE;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE internship_periods
        DROP CONSTRAINT internship_periods_persons CASCADE;
        """
    )