"""

ecdsa_keys_relations

Revision ID: fd170fae94ac
Creation date: 2023-09-08 20:26:09.232610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd170fae94ac'
down_revision = 'ffafefc9a15e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE ecdsa_keys
        ADD CONSTRAINT ecdsa_keys_to_persons
        FOREIGN KEY (owner_person_id) REFERENCES persons;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE ecdsa_keys
        DROP CONSTRAINT ecdsa_keys_to_persons CASCADE;
        """
    )
