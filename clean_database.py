#!/usr/bin/env python3
"""
Clean Database Script
Remove Bosnian questions and template functionality
"""

import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def clean_database():
    """Remove Bosnian questions and unnecessary template data"""
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///modern360.db')

    # Handle SQLite database
    if database_url.startswith('sqlite:///'):
        db_path = database_url.replace('sqlite:///', '')

        # Check common database locations
        if not os.path.exists(db_path):
            if os.path.exists(f"instance/{os.path.basename(db_path)}"):
                db_path = f"instance/{os.path.basename(db_path)}"
            else:
                print(f"❌ Database file not found: {db_path}")
                return

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("🧹 Cleaning database...")

        # Remove all predefined questions (Bosnian and template questions)
        cursor.execute("DELETE FROM question WHERE assessment_id IS NULL")
        deleted_questions = cursor.rowcount
        print(f"✅ Removed {deleted_questions} template/predefined questions")

        # Remove questions with Bosnian content (contains non-English characters)
        cursor.execute("""
            DELETE FROM question
            WHERE question_text LIKE '%ć%'
               OR question_text LIKE '%č%'
               OR question_text LIKE '%đ%'
               OR question_text LIKE '%š%'
               OR question_text LIKE '%ž%'
               OR question_text LIKE '%Ć%'
               OR question_text LIKE '%Č%'
               OR question_text LIKE '%Đ%'
               OR question_text LIKE '%Š%'
               OR question_text LIKE '%Ž%'
        """)
        deleted_bosnian = cursor.rowcount
        print(f"✅ Removed {deleted_bosnian} Bosnian questions")

        # Remove language column if it exists
        try:
            cursor.execute("SELECT language FROM question LIMIT 1")
            # If we get here, language column exists
            cursor.execute("ALTER TABLE question DROP COLUMN language")
            print("✅ Removed language column from question table")
        except sqlite3.OperationalError:
            print("ℹ️ Language column doesn't exist (already removed)")

        # Remove question_group column if it exists
        try:
            cursor.execute("SELECT question_group FROM question LIMIT 1")
            # If we get here, question_group column exists
            cursor.execute("ALTER TABLE question DROP COLUMN question_group")
            print("✅ Removed question_group column from question table")
        except sqlite3.OperationalError:
            print("ℹ️ Question_group column doesn't exist (already removed)")

        conn.commit()
        conn.close()

        print("🎉 Database cleaning completed!")

    else:
        print("❌ PostgreSQL cleaning not implemented yet")

if __name__ == "__main__":
    clean_database()