#!/usr/bin/env python3
"""
Create Demo Data for Testing
Add sample companies, users, and assessments
"""

import sqlite3
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def create_demo_data():
    """Create demo data for testing admin functionality"""
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

        print("🎯 Creating demo data...")

        # Clear existing demo data
        cursor.execute("DELETE FROM user WHERE email LIKE '%demo%'")
        cursor.execute("DELETE FROM company WHERE name LIKE '%Demo%'")

        # Create demo companies
        companies = [
            ("Tech Solutions Inc", "Leading technology consulting company"),
            ("Global Marketing Group", "International marketing and advertising agency"),
            ("Healthcare Systems Ltd", "Healthcare technology and services provider")
        ]

        company_ids = []
        for name, desc in companies:
            cursor.execute("""
                INSERT INTO company (name, description, created_at, is_active)
                VALUES (?, ?, ?, 1)
            """, (name, desc, datetime.utcnow()))
            company_ids.append(cursor.lastrowid)
            print(f"✅ Created company: {name}")

        # Create demo users for each company
        users_data = [
            # Tech Solutions Inc
            ("John Smith", "john.demo@techsolutions.com", "manager", company_ids[0]),
            ("Sarah Johnson", "sarah.demo@techsolutions.com", "user", company_ids[0]),
            ("Mike Davis", "mike.demo@techsolutions.com", "user", company_ids[0]),
            ("Lisa Chen", "lisa.demo@techsolutions.com", "user", company_ids[0]),

            # Global Marketing Group
            ("Emily Wilson", "emily.demo@globalmarketing.com", "manager", company_ids[1]),
            ("David Brown", "david.demo@globalmarketing.com", "user", company_ids[1]),
            ("Anna Garcia", "anna.demo@globalmarketing.com", "user", company_ids[1]),

            # Healthcare Systems Ltd
            ("Robert Taylor", "robert.demo@healthsystems.com", "manager", company_ids[2]),
            ("Jennifer Martinez", "jennifer.demo@healthsystems.com", "user", company_ids[2]),
            ("Kevin Anderson", "kevin.demo@healthsystems.com", "user", company_ids[2])
        ]

        user_ids = []
        for name, email, role, company_id in users_data:
            cursor.execute("""
                INSERT INTO user (name, email, role, company_id, created_at, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (name, email, role, company_id, datetime.utcnow()))
            user_ids.append(cursor.lastrowid)
            print(f"✅ Created user: {name} ({email})")

        # Create demo assessments
        assessments_data = [
            ("Leadership Skills Assessment", "Comprehensive evaluation of leadership capabilities", user_ids[0], company_ids[0]),
            ("Team Performance Review", "Annual team performance and collaboration assessment", user_ids[4], company_ids[1]),
            ("Customer Service Excellence", "Customer service skills and performance evaluation", user_ids[7], company_ids[2])
        ]

        assessment_ids = []
        for title, desc, creator_id, company_id in assessments_data:
            deadline = datetime.utcnow() + timedelta(days=30)
            cursor.execute("""
                INSERT INTO assessment (title, description, creator_id, company_id, created_at, deadline, is_active)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (title, desc, creator_id, company_id, datetime.utcnow(), deadline))
            assessment_id = cursor.lastrowid
            assessment_ids.append(assessment_id)
            print(f"✅ Created assessment: {title}")

            # Add sample questions to each assessment
            questions = [
                "How would you rate the communication skills?",
                "Evaluate the problem-solving abilities",
                "Rate the teamwork and collaboration",
                "Assess the leadership potential",
                "How well does this person handle pressure?"
            ]

            for i, question_text in enumerate(questions):
                cursor.execute("""
                    INSERT INTO question (assessment_id, question_text, question_type, `order`)
                    VALUES (?, ?, 'rating', ?)
                """, (assessment_id, question_text, i + 1))

            print(f"  ↳ Added {len(questions)} questions")

        conn.commit()
        conn.close()

        print(f"\n🎉 Demo data creation completed!")
        print(f"📊 Created:")
        print(f"   • {len(companies)} demo companies")
        print(f"   • {len(users_data)} demo users")
        print(f"   • {len(assessments_data)} demo assessments")
        print(f"   • {len(assessments_data) * 5} demo questions")

    else:
        print("❌ PostgreSQL demo data creation not implemented yet")

if __name__ == "__main__":
    create_demo_data()