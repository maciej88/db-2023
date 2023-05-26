"""

create table movie_languages

Revision ID: 9a5bd69dadde
Creation date: 2023-05-03 09:24:52.573019

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '9a5bd69dadde'
down_revision = 'f2fa8aa8906f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f"""
    --sql 
    CREATE TABLE movie_languages (
        movie_id INT NOT NULL,
        lang_id VARCHAR(2) NOT NULL,

        CONSTRAINT fk_movie_id FOREIGN KEY (movie_id)
            REFERENCES movies(movie_id),
        CONSTRAINT fk_lang_id FOREIGN KEY (lang_id)
            REFERENCES languages(lang_id)    
    )
""")


def downgrade() -> None:
    op.execute(f"""
    DROP TABLE IF EXISTS movie_languages CASCADE;
""")
