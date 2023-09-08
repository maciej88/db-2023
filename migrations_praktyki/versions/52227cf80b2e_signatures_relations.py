"""

signatures_relations

Revision ID: 52227cf80b2e
Creation date: 2023-09-08 20:44:47.136809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52227cf80b2e'
down_revision = 'fd170fae94ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE signatures
        ADD CONSTRAINT signatures_to_persons
        FOREIGN KEY (person_id) REFERENCES persons;
        ALTER TABLE ecdsa_keys
        ADD COLUMN signatures_id uuid;
        ALTER TABLE  ecdsa_keys
        ADD CONSTRAINT keys_signatures
        FOREIGN KEY (signatures_id) REFERENCES signatures (id)
        ON DELETE CASCADE;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE signatures
        DROP CONSTRAINT signatures_to_persons CASCADE;
        ALTER TABLE ecdsa_keys
        DROP CONSTRAINT keys_signatures;
        ALTER TABLE ecdsa_keys DROP COLUMN signatures_id
        """
    )
