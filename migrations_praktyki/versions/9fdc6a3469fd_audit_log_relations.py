"""

audit_log_relations

Revision ID: 9fdc6a3469fd
Creation date: 2023-09-08 21:34:48.202329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fdc6a3469fd'
down_revision = 'cb266a849744'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE audit_log
        ADD CONSTRAINT audit_log_to_companies
        FOREIGN KEY (author_of_log) REFERENCES companies;
        ALTER TABLE audit_log
        ADD CONSTRAINT audit_log_to_persons
        FOREIGN KEY (target_of_log) REFERENCES persons;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE audit_log
        DROP CONSTRAINT audit_log_to_companies CASCADE;
        ALTER TABLE audit_log
        DROP CONSTRAINT audit_log_to_persons CASCADE;
        """
    )
