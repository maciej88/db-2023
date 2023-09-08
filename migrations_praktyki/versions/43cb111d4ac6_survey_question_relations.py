"""

survey_question_relations

Revision ID: 43cb111d4ac6
Creation date: 2023-09-08 21:46:53.173932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43cb111d4ac6'
down_revision = '9fdc6a3469fd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE survey_question
        ADD CONSTRAINT survey_question_answer
        FOREIGN KEY (id) REFERENCES survey_answer;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE survey_question
        DROP CONSTRAINT survey_question_answer CASCADE;
        """
    )
