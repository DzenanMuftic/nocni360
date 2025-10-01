#!/usr/bin/env python3
"""
Migration script to restructure assessment responses from JSON to individual columns.
This creates a new table with explicit columns for each question response.
"""

from app import app, db
from sqlalchemy import text
import json

def migrate_responses():
    with app.app_context():
        print("Starting migration: JSON responses to individual columns...")

        # Step 1: Create new response table with individual columns
        print("\nStep 1: Creating new response_details table...")

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS response_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_response_id INTEGER NOT NULL,
            assessment_id INTEGER NOT NULL,
            invitation_id INTEGER,
            user_id INTEGER,
            respondent_email VARCHAR(120),
            assessment_title VARCHAR(200),
            submitted_at DATETIME,

            -- Question responses (q1-q39)
            q1 VARCHAR(10),
            q2 VARCHAR(10),
            q3 VARCHAR(10),
            q4 VARCHAR(10),
            q5 VARCHAR(10),
            q6 VARCHAR(10),
            q7 VARCHAR(10),
            q8 VARCHAR(10),
            q9 VARCHAR(10),
            q10 VARCHAR(10),
            q11 VARCHAR(10),
            q12 VARCHAR(10),
            q13 VARCHAR(10),
            q14 VARCHAR(10),
            q15 VARCHAR(10),
            q16 VARCHAR(10),
            q17 VARCHAR(10),
            q18 VARCHAR(10),
            q19 VARCHAR(10),
            q20 VARCHAR(10),
            q21 VARCHAR(10),
            q22 VARCHAR(10),
            q23 VARCHAR(10),
            q24 VARCHAR(10),
            q25 VARCHAR(10),
            q26 VARCHAR(10),
            q27 VARCHAR(10),
            q28 VARCHAR(10),
            q29 VARCHAR(10),
            q30 VARCHAR(10),
            q31 VARCHAR(10),
            q32 VARCHAR(10),
            q33 VARCHAR(10),
            q34 VARCHAR(10),
            q35 VARCHAR(10),
            q36 VARCHAR(10),
            q37 VARCHAR(10),
            q38 VARCHAR(10),
            q39 VARCHAR(10),

            FOREIGN KEY (assessment_response_id) REFERENCES assessment_response (id),
            FOREIGN KEY (assessment_id) REFERENCES assessment (id),
            FOREIGN KEY (invitation_id) REFERENCES invitation (id),
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
        """

        db.session.execute(text(create_table_sql))
        db.session.commit()
        print("✓ Table created successfully")

        # Step 2: Migrate existing data
        print("\nStep 2: Migrating existing response data...")

        # Get all existing responses
        existing_responses = db.session.execute(text("""
            SELECT
                ar.id,
                ar.assessment_id,
                ar.user_id,
                ar.invitation_id,
                ar.responses,
                ar.submitted_at,
                i.email as respondent_email,
                a.title as assessment_title
            FROM assessment_response ar
            LEFT JOIN invitation i ON ar.invitation_id = i.id
            LEFT JOIN assessment a ON ar.assessment_id = a.id
        """)).fetchall()

        print(f"Found {len(existing_responses)} responses to migrate")

        for response in existing_responses:
            # Parse JSON responses
            response_data = json.loads(response.responses)

            # Build column list and values
            columns = [
                'assessment_response_id',
                'assessment_id',
                'invitation_id',
                'user_id',
                'respondent_email',
                'assessment_title',
                'submitted_at'
            ]
            values = [
                response.id,
                response.assessment_id,
                response.invitation_id,
                response.user_id,
                response.respondent_email,
                response.assessment_title,
                response.submitted_at
            ]

            # Add question responses
            for i in range(1, 40):
                q_key = f'q{i}'
                columns.append(q_key)
                values.append(response_data.get(q_key))

            # Create placeholders for SQL
            placeholders = ', '.join([f':param{i}' for i in range(len(values))])
            columns_str = ', '.join(columns)

            insert_sql = f"""
                INSERT INTO response_details ({columns_str})
                VALUES ({placeholders})
            """

            # Create parameter dictionary
            params = {f'param{i}': value for i, value in enumerate(values)}
            db.session.execute(text(insert_sql), params)
            print(f"  ✓ Migrated response ID {response.id} from {response.respondent_email}")

        db.session.commit()
        print(f"\n✓ Successfully migrated {len(existing_responses)} responses")

        # Step 3: Verify migration
        print("\nStep 3: Verifying migration...")
        result = db.session.execute(text("SELECT COUNT(*) as count FROM response_details")).fetchone()
        print(f"✓ Total records in response_details: {result.count}")

        # Show sample data
        print("\nSample migrated data:")
        sample = db.session.execute(text("""
            SELECT
                id,
                respondent_email,
                assessment_title,
                q1, q2, q3, q4, q5,
                submitted_at
            FROM response_details
            LIMIT 2
        """)).fetchall()

        for row in sample:
            print(f"\nID: {row.id}")
            print(f"  Email: {row.respondent_email}")
            print(f"  Assessment: {row.assessment_title}")
            print(f"  First 5 answers: q1={row.q1}, q2={row.q2}, q3={row.q3}, q4={row.q4}, q5={row.q5}")
            print(f"  Submitted: {row.submitted_at}")

        print("\n" + "="*60)
        print("Migration completed successfully!")
        print("="*60)
        print("\nNew table 'response_details' has been created with:")
        print("  - Individual columns for each question (q1-q39)")
        print("  - Assessment metadata (title, ID)")
        print("  - Respondent information (email, user_id)")
        print("  - Timestamps (submitted_at)")
        print("\nThe original 'assessment_response' table is preserved.")

if __name__ == '__main__':
    migrate_responses()
