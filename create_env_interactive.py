#!/usr/bin/env python
import os
import getpass

def create_env_file():
    """Create a .env file with user input"""
    print("Creating .env file for the Blog CMS project...")
    
    # Get PostgreSQL password
    postgres_password = getpass.getpass("Enter PostgreSQL 'postgres' user password: ")
    
    # Get other configuration values
    debug = input("Enable debug mode? (y/n, default: y): ").lower() != 'n'
    secret_key = input("Enter a secret key (or press Enter for a default): ")
    if not secret_key:
        secret_key = "django-insecure-p4&t4m)l6oje8l8z9l2@lqy&#bwujg!81fc_pa8)+ec28dgrl3"
    
    # Get database configuration
    db_name = input("Enter database name (default: blog_cms): ") or "blog_cms"
    db_user = input("Enter database username (default: postgres): ") or "postgres"
    db_host = input("Enter database host (default: localhost): ") or "localhost"
    db_port = input("Enter database port (default: 5432): ") or "5432"
    
    # Format the DATABASE_URL
    db_url = f"postgresql://{db_user}:{postgres_password}@{db_host}:{db_port}/{db_name}"
    
    # Create the .env file
    with open('.env', 'w') as f:
        f.write(f"DEBUG={'True' if debug else 'False'}\n")
        f.write(f"SECRET_KEY={secret_key}\n")
        f.write("ALLOWED_HOSTS=localhost,127.0.0.1\n")
        f.write(f"DATABASE_URL={db_url}\n")
    
    print("\n.env file created successfully!")
    print("The file contains:")
    print(f"DEBUG={'True' if debug else 'False'}")
    print(f"SECRET_KEY=[hidden]")
    print("ALLOWED_HOSTS=localhost,127.0.0.1")
    print(f"DATABASE_URL=postgresql://{db_user}:[password-hidden]@{db_host}:{db_port}/{db_name}")
    
    print("\nNext steps:")
    print("1. Ensure PostgreSQL is running")
    print(f"2. Make sure the database '{db_name}' exists")
    print("3. Run 'python test_postgres_connection.py' to test the connection")
    print("4. Run 'python migrate_to_postgres.py' to migrate your data")

if __name__ == "__main__":
    create_env_file() 