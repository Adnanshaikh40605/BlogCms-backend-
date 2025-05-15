import os
import sys
import django
from django.conf import settings
import psycopg2
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv()

def test_connection():
    """Test the PostgreSQL database connection using credentials from .env file"""
    print("🔍 Testing database connection...")
    
    # Get credentials from environment variables
    db_name = os.getenv('DB_NAME', '')
    db_user = os.getenv('DB_USER', '')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', '')
    db_port = os.getenv('DB_PORT', '')
    database_url = os.getenv('DATABASE_URL', '')
    
    # Print configuration (hide password)
    print("\n⚙️ Configuration:")
    print(f"  Database: {db_name}")
    print(f"  User: {db_user}")
    print(f"  Host: {db_host}")
    print(f"  Port: {db_port}")
    
    # Test connection
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Execute a test query
        cursor.execute('SELECT version();')
        
        # Fetch the result
        db_version = cursor.fetchone()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        print("\n✅ Connection successful!")
        print(f"  PostgreSQL version: {db_version[0]}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\n🔍 Attempting to connect using DATABASE_URL...")
        
        try:
            # Try connecting using the DATABASE_URL
            conn = psycopg2.connect(database_url)
            
            # Create a cursor object
            cursor = conn.cursor()
            
            # Execute a test query
            cursor.execute('SELECT version();')
            
            # Fetch the result
            db_version = cursor.fetchone()
            
            # Close the cursor and connection
            cursor.close()
            conn.close()
            
            print("\n✅ Connection via DATABASE_URL successful!")
            print(f"  PostgreSQL version: {db_version[0]}")
            
            return True
        except Exception as e2:
            print(f"\n❌ Connection via DATABASE_URL failed: {e2}")
            return False

if __name__ == "__main__":
    # Run the test
    success = test_connection()
    
    if success:
        print("\n🎉 Your database connection is properly configured!")
        print("  You can now run your Django application with:")
        print("  python manage.py runserver")
    else:
        print("\n🛠️ Please check your database configuration in the .env file")
        print("  Ensure your Railway PostgreSQL service is running")
        print("  If using a proxy, verify the proxy is accessible from your network") 