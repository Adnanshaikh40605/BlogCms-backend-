import subprocess
import sys
import getpass

def run_command(command):
    """Run a command and return the output"""
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(f"Error: {result.stderr}")
        return False
    return True

def setup_postgres():
    """Set up PostgreSQL database for the project"""
    print("Setting up PostgreSQL database...")
    
    # Get PostgreSQL password
    postgres_password = getpass.getpass("Enter PostgreSQL 'postgres' user password: ")
    
    # Set PGPASSWORD environment variable
    import os
    os.environ['PGPASSWORD'] = postgres_password
    
    # Check if PostgreSQL is running
    print("Checking PostgreSQL connection...")
    if not run_command('psql -U postgres -c "SELECT version();"'):
        print("Failed to connect to PostgreSQL. Please make sure PostgreSQL is installed and running.")
        sys.exit(1)
    
    # Create database
    print("Creating database 'blog_cms'...")
    run_command('psql -U postgres -c "CREATE DATABASE blog_cms;"')
    
    # Test connection to the new database
    print("Testing connection to the new database...")
    if run_command('psql -U postgres -d blog_cms -c "SELECT current_database();"'):
        print("✅ Database created successfully!")
    else:
        print("❌ Failed to create database.")
        sys.exit(1)
    
    print("\nPostgreSQL setup completed successfully!")
    print("Now you can run the migration script:")
    print("    python migrate_to_postgres.py")

if __name__ == "__main__":
    setup_postgres() 