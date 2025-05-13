#!/usr/bin/env python
import os
import sys
import django
from dotenv import load_dotenv
import psycopg2
import time
import re

# Load environment variables
load_dotenv()

def test_connection():
    """Test the connection to PostgreSQL database"""
    print("Testing PostgreSQL connection...")
    
    # Get the DATABASE_URL from environment variables
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("ERROR: No DATABASE_URL environment variable found.")
        print("Please set a valid PostgreSQL DATABASE_URL in your environment or .env file.")
        sys.exit(1)
    
    # Mask password for display
    masked_url = re.sub(r'(:)([^@]+)(@)', r'\1********\3', db_url)
    print(f"Found DATABASE_URL: {masked_url}")
    
    try:
        # Create connection from components
        url_pattern = r'postgresql://([^:]+):([^@]+)@([^:/]+)(?::(\d+))?/(.+)'
        match = re.match(url_pattern, db_url)
        
        if not match:
            print("ERROR: DATABASE_URL format is invalid")
            print("Expected format: postgresql://username:password@host:port/database_name")
            sys.exit(1)
            
        user, password, host, port, db_name = match.groups()
        port = int(port) if port else 5432  # Default PostgreSQL port
        
        print(f"Attempting to connect to PostgreSQL at {host}:{port} with user '{user}' to database '{db_name}'")
        
        # Try to connect to the database
        start_time = time.time()
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        db_version = cursor.fetchone()
        cursor.close()
        conn.close()
        
        elapsed_time = time.time() - start_time
        print(f"✅ Connection successful!")
        print(f"Database version: {db_version[0]}")
        print(f"Connection time: {elapsed_time:.2f} seconds")
        
        # Test basic Django functionality with PostgreSQL
        print("\nTesting Django with PostgreSQL...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
        os.environ['DEBUG'] = 'False'  # Use PostgreSQL settings
        django.setup()
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table';")
            try:
                count = cursor.fetchone()[0]
                print("❌ ERROR: Django is still connected to SQLite!")
            except Exception:
                print("✅ Django is correctly configured to use PostgreSQL")
            
            try:
                cursor.execute("SELECT count(*) FROM pg_catalog.pg_tables WHERE schemaname='public';")
                table_count = cursor.fetchone()[0]
                print(f"✅ Found {table_count} tables in PostgreSQL database")
            except Exception as e:
                print(f"❌ ERROR querying PostgreSQL tables: {e}")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check if PostgreSQL server is running")
        print("2. Verify your DATABASE_URL format: postgresql://username:password@host:port/database_name")
        print("3. Ensure the database exists and the user has proper permissions")
        print("4. Check if any firewall is blocking the connection")
        sys.exit(1)

if __name__ == "__main__":
    test_connection() 