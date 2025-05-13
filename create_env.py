# Create .env file with the necessary settings
with open('.env', 'w') as f:
    f.write("DEBUG=True\n")
    f.write("SECRET_KEY=your-secret-key-here\n")
    f.write("ALLOWED_HOSTS=localhost,127.0.0.1\n")
    f.write("DATABASE_URL=postgres://postgres:postgres@localhost:5432/blog_cms\n")

print("Created .env file with the following content:")
with open('.env', 'r') as f:
    print(f.read()) 