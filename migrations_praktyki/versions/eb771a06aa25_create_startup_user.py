"""

create startup user

Revision ID: eb771a06aa25
Creation date: 2023-07-30 10:43:44.636863

"""
from uuid import UUID

from alembic import op
import sqlalchemy as sa

from src.praktyki.model import Role, Person

# DEFAULT USER DATA (note: remove in public deployments)
person_id = UUID("11111111-1111-1111-1111-111111111111")
name = 'Khabib'
email = 'tester@khabib.wtf'
phone = '+48 111 222 444'
# passwd = '222'
passwd = "$argon2id$v=19$m=65536,t=3,p=4$rM+YZDGlQZUF2UAdMvFMQw$Bz1mmh66RogTipjqsgYXGg3h8Rm0f1J8woLl9ULj1SI"
roles = "{3}"  # Role.ADMIN

p = Person(person_id=person_id, name=name, email=email, phone=phone, password=passwd, roles=[Role.ADMIN],
           studentid=None, album=None, wykladowcaid=None, company_id=None, uid_in_company=None)

# revision identifiers, used by Alembic.
revision = "eb771a06aa25"
down_revision = "da92dd8cf06c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f'''INSERT INTO persons(person_id, name, email, phone, password, roles) values 
        ('{p.person_id}', '{p.name}', '{p.email}', '{p.phone}', '{p.password}', '{roles}') ''')


def downgrade() -> None:
    op.execute(f"DELETE FROM persons WHERE email='{email}'")
