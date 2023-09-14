"""

relation_applications_curriculum_vitae

Revision ID: ffa6b01e1b8d
Creation date: 2023-09-09 13:16:14.593030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffa6b01e1b8d'
down_revision = '4cf82557cb6e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE  applications
        ADD CONSTRAINT applications_curriculum_vitae
        FOREIGN KEY (cv_id) REFERENCES curriculum_vitae ON DELETE CASCADE;
        """
    )

def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE applications
        DROP CONSTRAINT applications_curriculum_vitae CASCADE;
        """
    )
