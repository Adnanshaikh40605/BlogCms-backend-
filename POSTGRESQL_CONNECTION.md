# PostgreSQL Connection Details

This file contains the details needed to connect to your PostgreSQL database.

## Connection Information

- **Database Name:** `railway`
- **Username:** `postgres`
- **Password:** `TLgjKUteroESAXyyKSkzZeFBRitnmOLq`
- **Host:** `ballast.proxy.rlwy.net`
- **Port:** `17918`
- **PGDATA:** `/var/lib/postgresql/data/pgdata`

## Connection Strings

### External Connection String
```
postgresql://postgres:TLgjKUteroESAXyyKSkzZeFBRitnmOLq@ballast.proxy.rlwy.net:17918/railway
```

### Internal Railway Connection String
```
postgresql://postgres:TLgjKUteroESAXyyKSkzZeFBRitnmOLq@postgres.railway.internal:5432/railway
```

## Environment Variables for .env file

Copy the following lines to your `.env` file:

```
# PostgreSQL database settings
DB_NAME=railway
DB_USER=postgres
DB_PASSWORD=TLgjKUteroESAXyyKSkzZeFBRitnmOLq
DB_HOST=ballast.proxy.rlwy.net
DB_PORT=17918
DATABASE_URL=postgresql://postgres:TLgjKUteroESAXyyKSkzZeFBRitnmOLq@ballast.proxy.rlwy.net:17918/railway
INTERNAL_DB_URL=postgresql://postgres:TLgjKUteroESAXyyKSkzZeFBRitnmOLq@postgres.railway.internal:5432/railway
PGDATA=/var/lib/postgresql/data/pgdata
```

## Manual Database Setup

If you need to set up the database connection manually, use the following steps:

1. Open `backend/settings.py`
2. Update the `DATABASES` configuration with:
   
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'railway',
           'USER': 'postgres',
           'PASSWORD': 'TLgjKUteroESAXyyKSkzZeFBRitnmOLq',
           'HOST': 'ballast.proxy.rlwy.net',
           'PORT': '17918',
           'CONN_MAX_AGE': 60,
           'OPTIONS': {
               'connect_timeout': 5,
           },
       }
   }
   ```

## Testing the Connection

To test the database connection, run:

```
python backend/test_db_connection.py
```

This will attempt to connect using multiple methods and show you which ones succeed. 