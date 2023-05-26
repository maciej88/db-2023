"""

create table movie_p_companies

Revision ID: 80f883d33378
Creation date: 2023-05-03 10:25:45.793028

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '80f883d33378'
down_revision = 'bd4f5200f83a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f"""
    --sql 
    CREATE TABLE movie_prod_companies(
        movie_id INT,
        company_id INT,

        CONSTRAINT fk_movie_id FOREIGN KEY (movie_id)
            REFERENCES movies(movie_id),
        CONSTRAINT fk_company_id FOREIGN KEY (company_id)
            REFERENCES prod_companies(company_id) 
            );   
""")


def downgrade() -> None:
    op.execute(f"""
    DROP TABLE IF EXISTS movie_prod_companies CASCADE;
""")
