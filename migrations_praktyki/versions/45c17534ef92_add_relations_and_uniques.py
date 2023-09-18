"""

add_relations_and_uniques

Revision ID: 45c17534ef92
Creation date: 2023-09-18 20:26:40.789257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45c17534ef92'
down_revision = 'ffa6b01e1b8d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    --- add relations:
        ALTER TABLE ecdsa_keys 
        ADD CONSTRAINT ecdsa_keys_persons 
        FOREIGN KEY (owner_person_id) REFERENCES persons (person_id) ON DELETE CASCADE;
        ALTER TABLE signatures 
        ADD CONSTRAINT signatures_persons 
        FOREIGN KEY (person_id) REFERENCES persons (person_id) ON DELETE CASCADE;
        ALTER TABLE signatures 
        ADD CONSTRAINT signatures_ecdsa_keys 
        FOREIGN KEY (keyid) REFERENCES ecdsa_keys (key_id) ON DELETE SET NULL;
        ALTER TABLE signature_texts 
        ADD CONSTRAINT signature_texts_persons 
        FOREIGN KEY (person_id) REFERENCES persons (person_id) ON DELETE CASCADE;
        ALTER TABLE curriculum_vitae 
        ADD CONSTRAINT curriculum_vitae_persons 
        FOREIGN KEY (student_id) REFERENCES persons (person_id) ON DELETE CASCADE;
        ALTER TABLE days 
        ADD CONSTRAINT days_internship_periods 
        FOREIGN KEY (period_id) REFERENCES internship_periods (id) ON DELETE CASCADE;
        ALTER TABLE audit_log 
        ADD CONSTRAINT audit_log_persons_author 
        FOREIGN KEY (author_of_log) REFERENCES persons (person_id) ON DELETE CASCADE;
        ALTER TABLE audit_log 
        ADD CONSTRAINT audit_log_persons_author_target 
        FOREIGN KEY (target_of_log) REFERENCES persons (person_id) ON DELETE CASCADE;
        ALTER TABLE survey 
        ADD CONSTRAINT survey_internship_periods
        FOREIGN KEY (internship_period_id) REFERENCES internship_periods (id) ON DELETE CASCADE;
        ALTER TABLE internship_periods 
        ADD COLUMN agreement_id uuid;
        ALTER TABLE internship_periods 
        ADD CONSTRAINT internship_periods_agreements 
        FOREIGN KEY (agreement_id) REFERENCES internship_agreements (id) ON DELETE CASCADE;
        ALTER TABLE internship_periods 
        ADD CONSTRAINT internship_periods_persons 
        FOREIGN KEY (student_id) REFERENCES persons (person_id) ON DELETE CASCADE;
        ALTER TABLE applications 
        ADD CONSTRAINT applications_persons 
        FOREIGN KEY (student_id) REFERENCES persons (person_id) ON DELETE CASCADE;
        ALTER TABLE applications 
        ADD CONSTRAINT applications_curriculum_vitae 
        FOREIGN KEY (cv_id) REFERENCES curriculum_vitae (id) ON DELETE CASCADE;
        ALTER TABLE internships 
        ADD CONSTRAINT internships_persons 
        FOREIGN KEY (student_id) REFERENCES persons (person_id) ON DELETE CASCADE;
        ALTER TABLE internship_agreements 
        ADD CONSTRAINT internship_agreements_persons 
        FOREIGN KEY (student_id) REFERENCES persons (person_id) ON DELETE CASCADE;
        ALTER TABLE internship_agreements 
        ADD CONSTRAINT internship_agreements_applications 
        FOREIGN KEY (application_id) REFERENCES applications (id) ON DELETE CASCADE;
        ALTER TABLE period_final_reports 
        ADD CONSTRAINT period_final_reports_persons 
        FOREIGN KEY (student_id) REFERENCES persons (person_id) ON DELETE CASCADE;
        ALTER TABLE period_final_reports 
        ADD CONSTRAINT period_final_reports_internship_periods 
        FOREIGN KEY (period_id) REFERENCES internship_periods (id) ON DELETE CASCADE;
        ALTER TABLE persons 
        ADD CONSTRAINT persons_companies 
        FOREIGN KEY (company_id) REFERENCES companies (id) ON DELETE SET NULL;
    --- add uniques:
        ALTER TABLE survey 
        ADD CONSTRAINT unique_internship_period_id 
        UNIQUE (internship_period_id);
        ALTER TABLE applications 
        ADD CONSTRAINT unique_framework_agreement_id 
        UNIQUE (framework_agreement_id);
        ALTER TABLE internship_agreements 
        ADD CONSTRAINT unique_application_id 
        UNIQUE (application_id);
        ALTER TABLE days 
        ADD CONSTRAINT unique_period_id_date_at 
        UNIQUE (period_id, date_at);
        ALTER TABLE ecdsa_keys 
        ADD CONSTRAINT unique_key 
        UNIQUE (key);
        ALTER TABLE internships 
        ADD CONSTRAINT unique_student_id 
        UNIQUE (student_id);
        ALTER TABLE persons 
        ADD CONSTRAINT unique_company_id_uid_in_company 
        UNIQUE (company_id, uid_in_company);
        ALTER TABLE period_final_reports 
        ADD CONSTRAINT unique_period_id 
        UNIQUE (period_id);
        ALTER TABLE signature_texts 
        ADD CONSTRAINT unique_st_document_id_person_id 
        UNIQUE (document_id, person_id);
        ALTER TABLE signatures 
        ADD CONSTRAINT unique_document_id_person_id 
        UNIQUE (document_id, person_id);
    """)


def downgrade() -> None:
    op.execute("""
    --- drop relations:
        ALTER TABLE ecdsa_keys
        DROP CONSTRAINT ecdsa_keys_persons;
        ALTER TABLE signatures 
        DROP CONSTRAINT signatures_persons;
        ALTER TABLE signatures
        DROP CONSTRAINT signatures_ecdsa_keys;
        ALTER TABLE signature_texts 
        DROP CONSTRAINT signature_texts_persons;
        ALTER TABLE curriculum_vitae 
        DROP CONSTRAINT curriculum_vitae_persons;
        ALTER TABLE days 
        DROP CONSTRAINT days_internship_periods;
        ALTER TABLE audit_log 
        DROP CONSTRAINT audit_log_persons_author;
        ALTER TABLE audit_log 
        DROP CONSTRAINT audit_log_persons_author_target;
        ALTER TABLE survey 
        DROP CONSTRAINT survey_internship_periods;
        ALTER TABLE internship_periods 
        DROP CONSTRAINT internship_periods_agreements;
        ALTER TABLE internship_periods 
        DROP CONSTRAINT internship_periods_persons;
        ALTER TABLE internship_periods 
        DROP COLUMN agreement_id;
        ALTER TABLE applications 
        DROP CONSTRAINT applications_persons;
        ALTER TABLE applications 
        DROP CONSTRAINT applications_curriculum_vitae;
        ALTER TABLE internships 
        DROP CONSTRAINT internships_persons;
        ALTER TABLE internship_agreements 
        DROP CONSTRAINT internship_agreements_persons;
        ALTER TABLE internship_agreements 
        DROP CONSTRAINT internship_agreements_applications;
        ALTER TABLE period_final_reports 
        DROP CONSTRAINT period_final_reports_persons;
        ALTER TABLE period_final_reports 
        DROP CONSTRAINT period_final_reports_internship_periods;
        ALTER TABLE persons 
        DROP CONSTRAINT persons_companies;
    --- remove uniques:
        ALTER TABLE survey 
        DROP CONSTRAINT unique_internship_period_id;
        ALTER TABLE applications 
        DROP CONSTRAINT unique_framework_agreement_id;
        ALTER TABLE internship_agreements 
        DROP CONSTRAINT unique_application_id;
        ALTER TABLE days 
        DROP CONSTRAINT unique_period_id_date_at;
        ALTER TABLE ecdsa_keys 
        DROP CONSTRAINT unique_key;
        ALTER TABLE internships 
        DROP CONSTRAINT unique_student_id;
        ALTER TABLE persons 
        DROP CONSTRAINT unique_company_id_uid_in_company;
        ALTER TABLE period_final_reports 
        DROP CONSTRAINT unique_period_id;
        ALTER TABLE signature_texts 
        DROP CONSTRAINT unique_st_document_id_person_id;
    """)
