"""

days_relations

Revision ID: cb266a849744
Creation date: 2023-09-08 21:22:57.323774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb266a849744'
down_revision = 'e9cb8e05db26'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE  days
        ADD CONSTRAINT days_period
        FOREIGN KEY (period_id) REFERENCES period_final_reports ON DELETE CASCADE;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE days
        DROP CONSTRAINT days_period CASCADE;
        """
    )
