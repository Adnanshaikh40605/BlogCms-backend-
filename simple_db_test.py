#!/usr/bin/env python
import psycopg2
import getpass

def test_connection():
    """Test PostgreSQL connection directly"""
    print("Testing PostgreSQL connection...")
    
    # Get user input
    db_name = input("Database name (default: blog_cms): ") or "blog_cms"
    db_user = input("Database username (default: postgres): ") or "postgres"
    db_pass = getpass.getpass("Database password: ")
    db_host = input("Database host (default: localhost): ") or "localhost"
    db_port = input("Database port (default: 5432): ") or "5432"
    
    # Try to connect
    try:
        print(f"Connecting to PostgreSQL at {db_host}:{db_port} with user '{db_user}'...")
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port
        )
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        db_version = cursor.fetchone()
        cursor.close()
        conn.close()
        
        print(f"✅ Connection successful!")
        print(f"Database version: {db_version[0]}")
        
        # Update .env file
        with open('.env', 'w') as f:
            f.write("DEBUG=False\n")
            f.write("SECRET_KEY=django-insecure-p4&t4m)l6oje8l8z9l2@lqy&#bwujg!81fc_pa8)+ec28dgrl3\n")
            f.write("ALLOWED_HOSTS=localhost,127.0.0.1\n")
            f.write(f"DATABASE_URL=postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}\n")
            f.write("USE_SQLITE=False\n")
        
        print("\n.env file updated with working PostgreSQL connection")
        print("Now you can run: python migrate_to_postgres.py")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check if PostgreSQL server is running")
        print("2. Make sure the database exists")
        print("3. Verify the username and password")
        print("4. Check if any firewall is blocking the connection")

if __name__ == "__main__":
    test_connection() 