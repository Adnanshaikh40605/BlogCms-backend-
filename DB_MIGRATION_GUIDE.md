# Database Migration Guide: SQLite to PostgreSQL

This guide will help you migrate your data from SQLite to PostgreSQL for this Django project.

## Prerequisites

1. PostgreSQL installed and running
2. Python environment with project dependencies installed
3. Basic knowledge of Django and database concepts

## Setup PostgreSQL

1. Install PostgreSQL if you haven't already:
   - Windows: Download and install from https://www.postgresql.org/download/windows/
   - macOS: `brew install postgresql`
   - Linux: `sudo apt install postgresql postgresql-contrib`

2. Create a new PostgreSQL database:
   ```bash
   # Connect to PostgreSQL
   sudo -u postgres psql
   
   # Create database and user (in PostgreSQL shell)
   CREATE DATABASE blog_cms;
   CREATE USER blog_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE blog_cms TO blog_user;
   
   # Exit PostgreSQL shell
   \q
   ```

## Configure Environment Variables

1. Create or update your `.env` file based on the `env.example` template:
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=.railway.app,localhost,127.0.0.1
   DATABASE_URL=postgres://blog_user:your_password@localhost:5432/blog_cms
   ```

2. Make sure the `DATABASE_URL` follows this format:
   ```
   postgres://username:password@host:port/database_name
   ```

## Run the Migration Script

1. Make sure your SQLite database (`db.sqlite3`) is in the project root and contains your data.

2. Run the migration script from your project root:
   ```bash
   python migrate_to_postgres.py
   ```

3. The script will:
   - Check if your PostgreSQL credentials are valid
   - Export data from SQLite to a temporary JSON file
   - Configure Django to use PostgreSQL
   - Run migrations on PostgreSQL
   - Import data from the JSON file to PostgreSQL
   - Clean up temporary files

## Verify Migration

1. Update your `.env` file to use PostgreSQL permanently:
   ```
   DEBUG=False
   ```

2. Run the Django server:
   ```bash
   python manage.py runserver
   ```

3. Verify that your data is correctly showing in the application.

## Troubleshooting

If you encounter errors during migration:

1. **Database Connection Issues**: Double-check your PostgreSQL connection string in the `.env` file.
2. **Permission Errors**: Make sure your PostgreSQL user has proper permissions on the database.
3. **Migration Errors**: If Django migrations fail, check the error message for specific issues.

## Production Deployment

For production environments (Railway, Heroku, etc.), the application will automatically use the PostgreSQL database specified by the `DATABASE_URL` environment variable.

## Rollback Plan

If you need to revert to SQLite:

1. Set `DEBUG=True` in your `.env` file
2. Restart your application 