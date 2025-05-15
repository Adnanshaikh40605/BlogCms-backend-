import urllib.parse
import os

# Raw credentials and connection info
db_user = "postgres"
db_password = "TLgjKUteroESAXyyKSkzZeFBRitnmOLq"
db_name = "railway"
public_host = "ballast.proxy.rlwy.net"
public_port = 17918
internal_host = "postgres.railway.internal"
internal_port = 5432
pgdata_path = "/var/lib/postgresql/data/pgdata"
secret_key = "django-insecure-p4&t4m)l6oje8l8z9l2@lqy&#bwujg!81fc_pa8)+ec28dgrl3"

# Encode password
encoded_password = urllib.parse.quote(db_password)

# Build database URLs
DATABASE_URL = f"postgresql://{db_user}:{encoded_password}@{public_host}:{public_port}/{db_name}"
INTERNAL_DB_URL = f"postgresql://{db_user}:{encoded_password}@{internal_host}:{internal_port}/{db_name}"

# Compose .env content
env_content = f"""
# Django environment variables

# PostgreSQL database settings
DB_NAME={db_name}
DB_USER={db_user}
DB_PASSWORD={db_password}
DB_HOST={public_host}
DB_PORT={public_port}
DATABASE_URL={DATABASE_URL}
INTERNAL_DB_URL={INTERNAL_DB_URL}
PGDATA={pgdata_path}

# Other settings
DEBUG=False
SECRET_KEY={secret_key}
ALLOWED_HOSTS=localhost,127.0.0.1,web-production-f03ff.up.railway.app
USE_SQLITE=False
""".strip()

# Write to .env
with open(".env", "w") as f:
    f.write(env_content)

print("✅ .env file generated successfully!")
print("You can now run: python manage.py runserver") 