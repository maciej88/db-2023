"""

relation_internship_agreements_persons

Revision ID: 4cf82557cb6e
Creation date: 2023-09-09 13:04:23.193754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cf82557cb6e'
down_revision = '20ca9d489f50'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE  internship_agreements
        ADD CONSTRAINT internship_agreements_persons
        FOREIGN KEY (student_id) REFERENCES persons ON DELETE CASCADE;
        """
    )

def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE internship_agreements
        DROP CONSTRAINT internship_agreements_persons CASCADE;
        """
    )
