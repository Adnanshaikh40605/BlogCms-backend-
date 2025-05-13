#!/usr/bin/env python
import os
import sys
import subprocess
import django
from django.conf import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def configure_django():
    """Configure Django to use SQLite database temporarily"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    # Force SQLite as source database
    os.environ['USE_SQLITE'] = 'True'
    django.setup()

def migrate_to_postgres():
    """Migrate data from SQLite to PostgreSQL"""
    print("Starting migration from SQLite to PostgreSQL...")
    
    # 1. Make sure PostgreSQL credentials are set
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("ERROR: No DATABASE_URL environment variable found.")
        print("Please set a valid PostgreSQL DATABASE_URL in your environment or .env file.")
        print("Format: postgres://username:password@host:port/database_name")
        sys.exit(1)
    
    # 2. Create a temporary JSON dump of all data
    print("Dumping data from SQLite database...")
    dump_result = subprocess.run(
        ['python', 'manage.py', 'dumpdata', '--exclude', 'contenttypes', '--exclude', 'auth.permission', '--output', 'data_dump.json'],
        capture_output=True,
        text=True
    )
    
    if dump_result.returncode != 0:
        print(f"Error dumping data: {dump_result.stderr}")
        sys.exit(1)
    
    # 3. Configure Django to use PostgreSQL
    print("Switching to PostgreSQL database...")
    os.environ['DEBUG'] = 'False'  # This forces Django to use the PostgreSQL settings
    
    # 4. Run migrations on PostgreSQL
    print("Running migrations on PostgreSQL database...")
    migrate_result = subprocess.run(
        ['python', 'manage.py', 'migrate'],
        capture_output=True,
        text=True
    )
    
    if migrate_result.returncode != 0:
        print(f"Error running migrations: {migrate_result.stderr}")
        sys.exit(1)
    
    # 5. Load data into PostgreSQL
    print("Loading data into PostgreSQL...")
    load_result = subprocess.run(
        ['python', 'manage.py', 'loaddata', 'data_dump.json'],
        capture_output=True,
        text=True
    )
    
    if load_result.returncode != 0:
        print(f"Error loading data: {load_result.stderr}")
        sys.exit(1)
    
    # 6. Clean up
    os.remove('data_dump.json')
    
    print("Migration completed successfully!")
    print("Your data has been migrated from SQLite to PostgreSQL.")

if __name__ == "__main__":
    configure_django()
    migrate_to_postgres() 