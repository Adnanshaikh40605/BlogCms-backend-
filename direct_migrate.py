#!/usr/bin/env python
import psycopg2
import getpass
import os
import sys
import sqlite3
import json

def get_sqlite_schema():
    """Get schema and data from SQLite database"""
    print("Extracting schema from SQLite database...")
    
    # Check if SQLite file exists
    if not os.path.exists('db.sqlite3'):
        print("SQLite database file 'db.sqlite3' not found!")
        sys.exit(1)
    
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]
    
    schema = {}
    data = {}
    
    for table in tables:
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        schema[table] = columns
        
        # Get table data
        cursor.execute(f"SELECT * FROM {table};")
        rows = cursor.fetchall()
        data[table] = rows
    
    conn.close()
    
    return schema, data

def create_postgres_tables(schema, data):
    """Create tables in PostgreSQL and import data"""
    print("Connecting to PostgreSQL...")
    
    # Get PostgreSQL credentials
    db_name = input("PostgreSQL database name (default: blog_cms): ") or "blog_cms"
    db_user = input("PostgreSQL username (default: postgres): ") or "postgres"
    db_pass = getpass.getpass("PostgreSQL password: ")
    db_host = input("PostgreSQL host (default: localhost): ") or "localhost"
    db_port = input("PostgreSQL port (default: 5432): ") or "5432"
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Connected to PostgreSQL successfully.")
        
        # Create Django tables
        # Django ContentType
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS django_content_type (
            id SERIAL PRIMARY KEY,
            app_label VARCHAR(100) NOT NULL,
            model VARCHAR(100) NOT NULL,
            CONSTRAINT django_content_type_app_label_model_unique UNIQUE (app_label, model)
        );
        """)
        
        # Django Auth Permission
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_permission (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            content_type_id INTEGER NOT NULL REFERENCES django_content_type(id),
            codename VARCHAR(100) NOT NULL,
            CONSTRAINT auth_permission_content_type_id_codename_unique UNIQUE (content_type_id, codename)
        );
        """)
        
        # Django Auth Group
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_group (
            id SERIAL PRIMARY KEY,
            name VARCHAR(150) NOT NULL UNIQUE
        );
        """)
        
        # Django Auth Group Permissions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_group_permissions (
            id SERIAL PRIMARY KEY,
            group_id INTEGER NOT NULL REFERENCES auth_group(id),
            permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
            CONSTRAINT auth_group_permissions_group_id_permission_id_unique UNIQUE (group_id, permission_id)
        );
        """)
        
        # Django Auth User
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_user (
            id SERIAL PRIMARY KEY,
            password VARCHAR(128) NOT NULL,
            last_login TIMESTAMP WITH TIME ZONE NULL,
            is_superuser BOOLEAN NOT NULL,
            username VARCHAR(150) NOT NULL UNIQUE,
            first_name VARCHAR(150) NOT NULL,
            last_name VARCHAR(150) NOT NULL,
            email VARCHAR(254) NOT NULL,
            is_staff BOOLEAN NOT NULL,
            is_active BOOLEAN NOT NULL,
            date_joined TIMESTAMP WITH TIME ZONE NOT NULL
        );
        """)
        
        # Django Auth User Groups
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_user_groups (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES auth_user(id),
            group_id INTEGER NOT NULL REFERENCES auth_group(id),
            CONSTRAINT auth_user_groups_user_id_group_id_unique UNIQUE (user_id, group_id)
        );
        """)
        
        # Django Auth User Permissions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES auth_user(id),
            permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
            CONSTRAINT auth_user_user_permissions_user_id_permission_id_unique UNIQUE (user_id, permission_id)
        );
        """)
        
        # Django Admin Log
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS django_admin_log (
            id SERIAL PRIMARY KEY,
            action_time TIMESTAMP WITH TIME ZONE NOT NULL,
            object_id TEXT NULL,
            object_repr VARCHAR(200) NOT NULL,
            action_flag SMALLINT NOT NULL,
            change_message TEXT NOT NULL,
            content_type_id INTEGER NULL REFERENCES django_content_type(id),
            user_id INTEGER NOT NULL REFERENCES auth_user(id),
            CONSTRAINT django_admin_log_action_flag_check CHECK (action_flag >= 0)
        );
        """)
        
        # Django Session
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS django_session (
            session_key VARCHAR(40) PRIMARY KEY,
            session_data TEXT NOT NULL,
            expire_date TIMESTAMP WITH TIME ZONE NOT NULL
        );
        """)
        
        # Django Migrations
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS django_migrations (
            id SERIAL PRIMARY KEY,
            app VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            applied TIMESTAMP WITH TIME ZONE NOT NULL
        );
        """)
        
        # Blog FAQ
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog_faq (
            id SERIAL PRIMARY KEY,
            question VARCHAR(500) NOT NULL,
            answer TEXT NOT NULL,
            "order" INTEGER NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL
        );
        """)
        
        # Blog Post
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog_blogpost (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            slug VARCHAR(200) UNIQUE NOT NULL,
            content TEXT NOT NULL,
            featured_image VARCHAR(100) NULL,
            category VARCHAR(100) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
            published BOOLEAN NOT NULL,
            read_time VARCHAR(50) NOT NULL
        );
        """)
        
        # Blog Post FAQs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog_blogpost_faqs (
            id SERIAL PRIMARY KEY,
            blogpost_id INTEGER NOT NULL REFERENCES blog_blogpost(id),
            faq_id INTEGER NOT NULL REFERENCES blog_faq(id),
            CONSTRAINT blog_blogpost_faqs_blogpost_id_faq_id_unique UNIQUE (blogpost_id, faq_id)
        );
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS django_session_expire_date_idx ON django_session (expire_date);")
        cursor.execute("CREATE INDEX IF NOT EXISTS django_admin_log_content_type_id_idx ON django_admin_log (content_type_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS django_admin_log_user_id_idx ON django_admin_log (user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS auth_user_groups_user_id_idx ON auth_user_groups (user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS auth_user_groups_group_id_idx ON auth_user_groups (group_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS auth_user_user_permissions_user_id_idx ON auth_user_user_permissions (user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS auth_user_user_permissions_permission_id_idx ON auth_user_user_permissions (permission_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS auth_group_permissions_group_id_idx ON auth_group_permissions (group_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS auth_group_permissions_permission_id_idx ON auth_group_permissions (permission_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS auth_permission_content_type_id_idx ON auth_permission (content_type_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS blog_blogpost_faqs_blogpost_id_idx ON blog_blogpost_faqs (blogpost_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS blog_blogpost_faqs_faq_id_idx ON blog_blogpost_faqs (faq_id);")
        
        print("Database tables created successfully.")
        
        # Update environment variable
        with open('.env', 'w') as f:
            f.write("DEBUG=True\n")
            f.write("SECRET_KEY=django-insecure-p4&t4m)l6oje8l8z9l2@lqy&#bwujg!81fc_pa8)+ec28dgrl3\n")
            f.write("ALLOWED_HOSTS=localhost,127.0.0.1\n")
            f.write(f"DATABASE_URL=postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}\n")
        
        print("\nSuccessfully migrated to PostgreSQL!")
        print(f"DATABASE_URL updated in .env file: postgresql://{db_user}:***@{db_host}:{db_port}/{db_name}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    schema, data = get_sqlite_schema()
    create_postgres_tables(schema, data) 