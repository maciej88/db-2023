"""

relation_period_final_persons

Revision ID: 20ca9d489f50
Creation date: 2023-09-09 12:57:58.488342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20ca9d489f50'
down_revision = 'c9e1e3af65e4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE  period_final_reports
        ADD CONSTRAINT period_final_reports_persons
        FOREIGN KEY (student_id) REFERENCES persons ON DELETE CASCADE;
        """
    )

def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE period_final_reports
        DROP CONSTRAINT period_final_reports_persons CASCADE;
        """
    )
