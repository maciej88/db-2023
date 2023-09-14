"""

relation_signature_texts_persons

Revision ID: dc662c242256
Creation date: 2023-09-09 12:39:01.553572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc662c242256'
down_revision = '30ac651782d2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE  signature_texts
        ADD CONSTRAINT signature_texts_persons
        FOREIGN KEY (person_id) REFERENCES persons ON DELETE CASCADE;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE signature_texts
        DROP CONSTRAINT signature_texts_persons CASCADE;
        """
    )
