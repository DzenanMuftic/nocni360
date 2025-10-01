#!/usr/bin/env python3
"""
Modern360 Assessment - WSGI Application Entry Point
This file is used by deployment platforms like Render, Heroku, etc.
Serves both main app and admin app on same port with /pravo prefix routing
"""

import os
from dotenv import load_dotenv
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound

# Load environment variables
load_dotenv()

# Import the main application
from app import app

# Import admin application
from admin_app import admin_app

# Create combined WSGI application
# Main app serves root /, admin app serves /pravo/*
application = DispatcherMiddleware(app, {
    '/pravo': admin_app
})

if __name__ == "__main__":
    # This runs when file is executed directly (not recommended for production)
    port = int(os.environ.get('PORT', 9000))
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', port, application, use_reloader=False, use_debugger=False)
