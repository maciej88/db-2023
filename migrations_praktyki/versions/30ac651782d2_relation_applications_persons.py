"""

relation_applications_persons

Revision ID: 30ac651782d2
Creation date: 2023-09-09 12:35:12.677900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30ac651782d2'
down_revision = 'e9ccd9c93278'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE  applications
        ADD CONSTRAINT applications_persons
        FOREIGN KEY (student_id) REFERENCES persons ON DELETE CASCADE;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE applications
        DROP CONSTRAINT applications_persons CASCADE;
        """
    )
