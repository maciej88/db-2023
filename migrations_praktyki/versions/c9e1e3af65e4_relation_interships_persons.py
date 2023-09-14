"""

relation_internships_persons

Revision ID: c9e1e3af65e4
Creation date: 2023-09-09 12:50:49.498837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9e1e3af65e4'
down_revision = 'dc662c242256'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE  internships
        ADD CONSTRAINT internships_persons
        FOREIGN KEY (student_id) REFERENCES persons ON DELETE CASCADE;
        """
    )

def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE internships
        DROP CONSTRAINT internships_persons CASCADE;
        """
    )
