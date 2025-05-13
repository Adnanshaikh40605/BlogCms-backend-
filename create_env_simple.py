#!/usr/bin/env python

# Create a simple .env file with PostgreSQL connection
with open('.env', 'w') as f:
    f.write("DEBUG=True\n")
    f.write("SECRET_KEY=django-insecure-p4&t4m)l6oje8l8z9l2@lqy&#bwujg!81fc_pa8)+ec28dgrl3\n")
    f.write("ALLOWED_HOSTS=localhost,127.0.0.1\n")
    f.write("DATABASE_URL=postgresql://postgres:postgres@localhost:5432/blog_cms\n")

print("Created .env file with PostgreSQL connection")
print("Contents:")
print("DEBUG=True")
print("SECRET_KEY=[hidden]")
print("ALLOWED_HOSTS=localhost,127.0.0.1")
print("DATABASE_URL=postgresql://postgres:[password-hidden]@localhost:5432/blog_cms") 