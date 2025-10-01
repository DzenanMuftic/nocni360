# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Modern360 Assessment Platform - A professional 360-degree feedback platform built with Flask, featuring email-based authentication, assessment creation, and comprehensive admin panel.

## Development Commands

### Setup and Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Running the Application
```bash
# Universal startup script (recommended)
python start.py --mode=dev          # Development mode (both apps)
python start.py --mode=main         # Combined app (main + admin on port 9000)
python start.py --mode=admin        # Admin app only (legacy, use main instead)

# WSGI combined application (recommended)
python wsgi.py                      # Combined main + admin apps on port 9000

# Direct execution (legacy)
python app.py                       # Main application only
python admin_app.py                 # Admin dashboard only

# Setup database
python start.py --setup-db          # Initialize database tables
```

### Application Architecture
- **Combined Deployment**: Both apps run on port 9000 via WSGI dispatcher
- **Main App**: http://localhost:9000/ (root path)
- **Admin App**: http://localhost:9000/pravo (prefix path)
- **Single Port**: No separate ports needed, routing handled by WSGI middleware

### Database Operations
```bash
# Initialize database (first time)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Check database contents
python check_database.py

# Add predefined questions/templates
python add_question_templates.py
python add_predefined_questions.py
```

### Testing and Validation
```bash
# Test email configuration
python test_email.py

# Check database setup
python check_database.py

# Test specific email providers
python test_impactai_email.py
```

### Build and Deployment
```bash
# Build for production (Render.com)
./build.sh

# Local build simulation
bash build.sh
```

## Architecture Overview

### Combined Application Structure
- **Main App** (`app.py`): Public-facing assessment platform (root path `/`)
- **Admin App** (`admin_app.py`): Administrative dashboard (`/pravo` prefix)
- **WSGI Dispatcher** (`wsgi.py`): Routes requests to appropriate app based on path
- **Shared Database**: Both applications use the same database schema
- **Single Port**: Both apps accessible on port 9000 with path-based routing

### Core Components

#### Database Models (app.py:49-150)
- `User`: User accounts with email authentication
- `Assessment`: 360-degree assessment definitions
- `Question`: Individual assessment questions
- `Response`: User responses to assessments
- `Invitation`: Email invitation tracking
- `VerificationCode`: Email verification system

#### Authentication System
- **Email-based authentication** with 6-digit verification codes
- **Direct login links** in emails for instant access
- **No OAuth dependency** - uses Flask sessions
- **15-minute code expiration** for security

#### Email System
- Flask-Mail integration with SMTP support
- Gmail App Password authentication
- Professional invitation templates
- Verification code delivery

### Key Features

#### Assessment Management
- Create custom 360-degree assessments
- Pre-built question templates (Leadership, Communication, Teamwork)
- Deadline management and progress tracking
- Bulk invitation system with secure tokens

#### Admin Dashboard Features
- User management (create, edit, delete)
- Company management
- Assessment administration
- Invitation tracking and bulk sending
- Question template management
- Comprehensive reporting

## File Structure and Responsibilities

### Core Application Files
- `app.py` - Main Flask application (750+ lines)
- `admin_app.py` - Admin dashboard application (1400+ lines)
- `start.py` - Universal startup and deployment script

### Database and Migration
- `setup_database.py` - Database initialization
- `migrate_*.py` - Database migration scripts
- Migration scripts for adding language support, company fields, etc.

### Template Organization
- `templates/` - Main application templates (8 files)
- `admin_templates/` - Admin dashboard templates (15 files)
- `base.html` and `admin_base.html` - Base templates with Bootstrap 5

### Configuration and Deployment
- `.env.example` - Environment variables template
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development dependencies
- `Procfile` - Render.com deployment configuration
- `build.sh` - Build script for deployment
- `render.yaml` - Infrastructure as code

### Utility Scripts
- `add_question_templates.py` - Populate question templates
- `ensure_template_questions.py` - Ensure question data integrity
- `test_email.py` - Email configuration testing
- `gunicorn_*.py` - Production server configuration

## Environment Configuration

### Required Environment Variables
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///modern360.db  # or PostgreSQL URL
PORT=9000                           # Application port (default 9000)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### Email Setup Requirements
- Gmail account with 2-Factor Authentication enabled
- Gmail App Password (16-character, not regular password)
- SMTP settings configured for Gmail or alternative provider

## Development Workflow

### Local Development Setup
1. Clone repository and install dependencies
2. Copy `.env.example` to `.env` and configure (set PORT=9000)
3. Run `python start.py --setup-db` to initialize database
4. Run `python start.py --mode=main` for combined application
5. Access main app at http://localhost:9000, admin at http://localhost:9000/pravo

### Database Management
- Uses SQLAlchemy ORM with Flask-Migrate
- Supports both SQLite (development) and PostgreSQL (production)
- Migration scripts handle schema updates
- Utility scripts populate default data

### Code Conventions
- Flask application factory pattern
- Environment-based configuration
- Comprehensive error handling
- Professional email templates
- Bootstrap 5 with Material Design principles

## Deployment

### Render.com Deployment
- Configured via `Procfile` with web and admin processes
- Build script (`build.sh`) handles dependency installation and database setup
- Automatic PostgreSQL database provisioning
- Environment variables set through Render dashboard

### Production Considerations
- Gunicorn WSGI server for production
- Database connection pooling
- Email delivery through configured SMTP
- Security headers and session management
- Error logging and monitoring ready

## Admin Credentials
- Default admin login: `admin` / `admin123`
- Change these credentials in production deployment
- Admin dashboard provides full platform management capabilities