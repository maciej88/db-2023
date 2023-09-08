"""

uuid_for_persons_student

Revision ID: a12914d6ed97
Creation date: 2023-09-08 22:11:53.943177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a12914d6ed97'
down_revision = '43cb111d4ac6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE persons RENAME COLUMN studentid TO student_id;
    ALTER TABLE persons
    ALTER COLUMN student_id TYPE UUID USING student_id::UUID;   
               """)


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE persons
        ALTER COLUMN student_id TYPE INTEGER USING student_id::INTEGER; 
        ALTER TABLE persons RENAME COLUMN student_id TO studentid
        """
    )
