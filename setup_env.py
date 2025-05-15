#!/usr/bin/env python
"""
Setup environment variables for PostgreSQL connection.
This script creates a .env file with the necessary environment variables.
"""

import os
import sys
import re

def write_env_file(env_file_path=".env"):
    """Write PostgreSQL connection details to .env file"""
    
    # PostgreSQL connection details
    db_details = {
        "DB_NAME": "railway",
        "DB_USER": "postgres",
        "DB_PASSWORD": "TLgjKUteroESAXyyKSkzZeFBRitnmOLq",
        "DB_HOST": "ballast.proxy.rlwy.net",
        "DB_PORT": "17918",
        "DATABASE_URL": "postgresql://postgres:TLgjKUteroESAXyyKSkzZeFBRitnmOLq@ballast.proxy.rlwy.net:17918/railway",
        "INTERNAL_DB_URL": "postgresql://postgres:TLgjKUteroESAXyyKSkzZeFBRitnmOLq@postgres.railway.internal:5432/railway",
        "PGDATA": "/var/lib/postgresql/data/pgdata"
    }
    
    # Check if file exists and read existing content
    existing_vars = {}
    if os.path.exists(env_file_path):
        with open(env_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    existing_vars[key.strip()] = value.strip()
    
    # Merge new variables with existing ones
    all_vars = {**existing_vars, **db_details}
    
    # Write .env file
    with open(env_file_path, 'w') as f:
        f.write("# Django environment variables\n")
        
        # Write PostgreSQL details with a comment header
        f.write("\n# PostgreSQL database settings\n")
        for key, value in db_details.items():
            f.write(f"{key}={value}\n")
        
        # Write any other existing variables that aren't in the db_details
        other_vars = {k: v for k, v in existing_vars.items() if k not in db_details}
        if other_vars:
            f.write("\n# Other settings\n")
            for key, value in other_vars.items():
                f.write(f"{key}={value}\n")
        
    print(f"✅ Environment variables written to {env_file_path}")
    print(f"  Database: {db_details['DB_NAME']}")
    print(f"  Host: {db_details['DB_HOST']}")
    print(f"  Port: {db_details['DB_PORT']}")
    print(f"  User: {db_details['DB_USER']}")

def main():
    """Main function to run the script"""
    print("=" * 50)
    print("SETTING UP POSTGRESQL ENVIRONMENT VARIABLES")
    print("=" * 50)
    
    # Determine environment file path
    env_file = ".env"
    print(f"Current working directory: {os.getcwd()}")
    print(f"Writing environment variables to: {os.path.abspath(env_file)}")
    
    try:
        write_env_file(env_file)
        print("\n✅ Setup complete!")
        print("You can now run 'python manage.py runserver' to start the development server.")
    except Exception as e:
        print(f"\n❌ Error creating .env file: {str(e)}")
        print("Please check file permissions and try again.")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 