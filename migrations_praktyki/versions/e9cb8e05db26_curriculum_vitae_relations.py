"""

curriculum_vitae_relations

Revision ID: e9cb8e05db26
Creation date: 2023-09-08 21:08:02.403630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9cb8e05db26'
down_revision = '52227cf80b2e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE curriculum_vitae RENAME COLUMN student_id TO studentid;
        ALTER TABLE  curriculum_vitae
        ADD CONSTRAINT curriculum_vitae_persons
        FOREIGN KEY (studentid) REFERENCES persons ON DELETE CASCADE;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE curriculum_vitae
        DROP CONSTRAINT curriculum_vitae_persons CASCADE;
        ALTER TABLE curriculum_vitae RENAME COLUMN studentid TO student_id
        """
    )
