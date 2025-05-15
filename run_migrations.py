#!/usr/bin/env python
import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_migrations():
    """Run Django migrations to create database tables"""
    print("🔍 Setting up Django environment...")
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()
    
    print("🚀 Running migrations...")
    
    # Import the migrate command
    from django.core.management import execute_from_command_line
    
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("\n✅ Migrations completed successfully!")
    return True

if __name__ == "__main__":
    run_migrations()
    
    # Create a superuser if requested
    if '--create-superuser' in sys.argv:
        print("\n📝 Creating superuser...")
        from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperUserCommand
        from django.core.management import call_command
        
        # Check if environment variables are set for non-interactive creation
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
        
        if username and email and password:
            print(f"  Creating superuser with username: {username}")
            call_command(
                'createsuperuser',
                interactive=False,
                username=username,
                email=email
            )
            print("✅ Superuser created successfully!")
        else:
            print("  Running interactive superuser creation...")
            call_command('createsuperuser') 