#!/usr/bin/env python3
"""
Test Admin Functions
Systematically test all admin endpoints and functionality
"""

import requests
import json
import sys
from time import sleep

BASE_URL = "http://95.217.222.62:9000"
ADMIN_BASE = f"{BASE_URL}/pravo"

class AdminTester:
    def __init__(self):
        self.session = requests.Session()
        self.errors = []
        self.successes = []

    def log_success(self, test_name):
        print(f"✅ {test_name}")
        self.successes.append(test_name)

    def log_error(self, test_name, error):
        print(f"❌ {test_name}: {error}")
        self.errors.append(f"{test_name}: {error}")

    def test_main_app_access(self):
        """Test main app accessibility"""
        try:
            response = self.session.get(BASE_URL)
            if response.status_code == 200:
                self.log_success("Main app accessible")
            else:
                self.log_error("Main app access", f"Status {response.status_code}")
        except Exception as e:
            self.log_error("Main app access", str(e))

    def test_admin_login_page(self):
        """Test admin login page"""
        try:
            response = self.session.get(f"{ADMIN_BASE}/login")
            if response.status_code == 200 and "login" in response.text.lower():
                self.log_success("Admin login page accessible")
            else:
                self.log_error("Admin login page", f"Status {response.status_code}")
        except Exception as e:
            self.log_error("Admin login page", str(e))

    def test_admin_login(self):
        """Test admin login functionality"""
        try:
            # Get login page first for any CSRF tokens
            login_page = self.session.get(f"{ADMIN_BASE}/login")

            login_data = {
                'username': 'admin',
                'password': 'admin123'
            }

            response = self.session.post(f"{ADMIN_BASE}/login", data=login_data)

            if response.status_code == 302 or "dashboard" in response.url:
                self.log_success("Admin login successful")
                return True
            else:
                self.log_error("Admin login", f"Status {response.status_code}")
                return False
        except Exception as e:
            self.log_error("Admin login", str(e))
            return False

    def test_admin_dashboard(self):
        """Test admin dashboard access"""
        try:
            response = self.session.get(f"{ADMIN_BASE}/dashboard")
            if response.status_code == 200 and "dashboard" in response.text.lower():
                self.log_success("Admin dashboard accessible")
            else:
                self.log_error("Admin dashboard", f"Status {response.status_code}")
        except Exception as e:
            self.log_error("Admin dashboard", str(e))

    def test_companies_page(self):
        """Test companies management page"""
        try:
            response = self.session.get(f"{ADMIN_BASE}/companies")
            if response.status_code == 200:
                self.log_success("Companies page accessible")
                # Check for demo data
                if "Tech Solutions Inc" in response.text:
                    self.log_success("Demo companies visible")
                else:
                    self.log_error("Demo companies", "Not found in page")
            else:
                self.log_error("Companies page", f"Status {response.status_code}")
        except Exception as e:
            self.log_error("Companies page", str(e))

    def test_users_page(self):
        """Test users management page"""
        try:
            response = self.session.get(f"{ADMIN_BASE}/users")
            if response.status_code == 200:
                self.log_success("Users page accessible")
                # Check for demo data
                if "john.demo@techsolutions.com" in response.text:
                    self.log_success("Demo users visible")
                else:
                    self.log_error("Demo users", "Not found in page")
            else:
                self.log_error("Users page", f"Status {response.status_code}")
        except Exception as e:
            self.log_error("Users page", str(e))

    def test_assessments_page(self):
        """Test assessments management page"""
        try:
            response = self.session.get(f"{ADMIN_BASE}/assessments")
            if response.status_code == 200:
                self.log_success("Assessments page accessible")
                # Check for demo data
                if "Leadership Skills Assessment" in response.text:
                    self.log_success("Demo assessments visible")
                else:
                    self.log_error("Demo assessments", "Not found in page")
            else:
                self.log_error("Assessments page", f"Status {response.status_code}")
        except Exception as e:
            self.log_error("Assessments page", str(e))

    def test_create_company_page(self):
        """Test create company page"""
        try:
            response = self.session.get(f"{ADMIN_BASE}/companies/create")
            if response.status_code == 200:
                self.log_success("Create company page accessible")
            else:
                self.log_error("Create company page", f"Status {response.status_code}")
        except Exception as e:
            self.log_error("Create company page", str(e))

    def test_create_user_page(self):
        """Test create user page"""
        try:
            response = self.session.get(f"{ADMIN_BASE}/users/create")
            if response.status_code == 200:
                self.log_success("Create user page accessible")
            else:
                self.log_error("Create user page", f"Status {response.status_code}")
        except Exception as e:
            self.log_error("Create user page", str(e))

    def test_create_assessment_page(self):
        """Test create assessment page"""
        try:
            response = self.session.get(f"{ADMIN_BASE}/assessments/create")
            if response.status_code == 200:
                self.log_success("Create assessment page accessible")
            else:
                self.log_error("Create assessment page", f"Status {response.status_code}")
        except Exception as e:
            self.log_error("Create assessment page", str(e))

    def test_api_endpoints(self):
        """Test API endpoints"""
        # Test companies API
        try:
            response = self.session.get(f"{ADMIN_BASE}/api/companies")
            if response.status_code == 200 or response.status_code == 405:  # 405 = Method not allowed (GET on POST endpoint)
                self.log_success("Companies API endpoint reachable")
            else:
                self.log_error("Companies API", f"Status {response.status_code}")
        except Exception as e:
            self.log_error("Companies API", str(e))

        # Test users API
        try:
            response = self.session.get(f"{ADMIN_BASE}/api/users")
            if response.status_code == 200 or response.status_code == 405:
                self.log_success("Users API endpoint reachable")
            else:
                self.log_error("Users API", f"Status {response.status_code}")
        except Exception as e:
            self.log_error("Users API", str(e))

    def run_all_tests(self):
        """Run all tests systematically"""
        print("🧪 Starting comprehensive admin functionality tests...\n")

        # Basic connectivity
        self.test_main_app_access()
        self.test_admin_login_page()

        # Authentication
        if self.test_admin_login():
            # Authenticated pages
            self.test_admin_dashboard()
            self.test_companies_page()
            self.test_users_page()
            self.test_assessments_page()

            # Create pages
            self.test_create_company_page()
            self.test_create_user_page()
            self.test_create_assessment_page()

            # API endpoints
            self.test_api_endpoints()
        else:
            print("⚠️ Skipping authenticated tests due to login failure")

        # Results
        print(f"\n📊 Test Results:")
        print(f"✅ Passed: {len(self.successes)}")
        print(f"❌ Failed: {len(self.errors)}")

        if self.errors:
            print(f"\n🚨 Failures:")
            for error in self.errors:
                print(f"  • {error}")
            return False
        else:
            print(f"\n🎉 All tests passed!")
            return True

if __name__ == "__main__":
    tester = AdminTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)