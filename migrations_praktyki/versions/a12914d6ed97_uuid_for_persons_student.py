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
    ALTER TABLE curriculum_vitae
    DROP CONSTRAINT curriculum_vitae_persons CASCADE;
    
    ALTER TABLE persons DROP COLUMN IF EXISTS studentid;
    
    ALTER TABLE persons ADD COLUMN student_id uuid UNIQUE;
    
    ALTER TABLE curriculum_vitae DROP COLUMN IF EXISTS studentid;
    
    ALTER TABLE curriculum_vitae ADD COLUMN student_id uuid UNIQUE;
    
    ALTER TABLE curriculum_vitae
    ADD CONSTRAINT curriculum_vitae_persons
    FOREIGN KEY (student_id) REFERENCES persons (student_id) ON DELETE CASCADE;
       
               """)


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE curriculum_vitae
        DROP CONSTRAINT curriculum_vitae_persons CASCADE;
        
        ALTER TABLE curriculum_vitae DROP COLUMN IF EXISTS student_id;
        
        ALTER TABLE curriculum_vitae ADD COLUMN studentid uuid;
        
        ALTER TABLE persons DROP COLUMN IF EXISTS student_id;
        
        ALTER TABLE persons ADD COLUMN studentid INTEGER;
        
        ALTER TABLE  curriculum_vitae
        ADD CONSTRAINT curriculum_vitae_persons
        FOREIGN KEY (studentid) REFERENCES persons ON DELETE CASCADE;
        """
    )
