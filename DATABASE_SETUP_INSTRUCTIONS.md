# PostgreSQL Setup Instructions for Blog CMS

## Step 1: Install PostgreSQL

1. Download PostgreSQL for Windows:
   - Go to https://www.postgresql.org/download/windows/
   - Click on the "Download the installer" button
   - Select the latest version for Windows

2. Run the installer:
   - Accept the default installation directory
   - Choose the components to install (select all for simplicity)
   - Choose a data directory (accept default)
   - Set a password for the 'postgres' superuser
   - Set the port (default is 5432)
   - Select the default locale
   - Click "Next" to start the installation

3. Verify the installation:
   - The installer will install PostgreSQL and pgAdmin
   - Launch pgAdmin from the Start menu
   - Connect to the server using the password you set

## Step 2: Create a Database

1. Using pgAdmin:
   - Open pgAdmin
   - Connect to the PostgreSQL server (enter your password)
   - Right-click on "Databases" and select "Create" > "Database..."
   - Enter "blog_cms" as the database name
   - Click "Save"

2. Using command line:
   - Open Command Prompt or PowerShell
   - Run: `psql -U postgres -c "CREATE DATABASE blog_cms;"`
   - Enter your password when prompted

## Step 3: Update Environment Variables

1. Create or update your `.env` file:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgresql://postgres:YourPasswordHere@localhost:5432/blog_cms
   ```

   Replace `YourPasswordHere` with the password you set for the 'postgres' user.

2. Verify the format:
   - Make sure the DATABASE_URL has the format: `postgresql://username:password@host:port/database_name`
   - Note that we're using `postgresql://` instead of `postgres://` for better compatibility

## Step 4: Test the Connection

1. Run the connection test script:
   ```
   python test_postgres_connection.py
   ```

   This will attempt to connect to PostgreSQL using the credentials in your `.env` file.

## Step 5: Run the Migration

1. When the connection test passes, run the migration script:
   ```
   python migrate_to_postgres.py
   ```

   This will:
   - Export data from SQLite to a temporary JSON file
   - Create tables in PostgreSQL
   - Import data from the JSON file to PostgreSQL

## Troubleshooting

1. Connection Issues:
   - Ensure PostgreSQL service is running
   - Check that the password in DATABASE_URL matches your PostgreSQL password
   - Verify the port is correct (default is 5432)
   - Try connecting with pgAdmin to confirm your credentials work

2. Database Creation Issues:
   - If the database already exists, the script will show an error but continue
   - If you don't have permission to create a database, create it manually using pgAdmin

3. Common Error Messages:
   - "no module named 'psycopg2'": Run `pip install psycopg2-binary`
   - "Connection refused": PostgreSQL service is not running
   - "Authentication failed": Incorrect password
   - "Database does not exist": Create the database manually using pgAdmin 