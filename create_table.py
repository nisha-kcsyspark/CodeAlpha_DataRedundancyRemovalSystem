import boto3
import psycopg

host = "codealpha-data-redundancy-removal-system.cluster-czqok2wc0j7j.ap-south-1.rds.amazonaws.com"
port = 5432
database = "postgres"
user = "postgres"
region = "ap-south-1"

rds = boto3.client("rds", region_name=region)

token = rds.generate_db_auth_token(
    DBHostname=host,
    Port=port,
    DBUsername=user,
    Region=region
)

connection = psycopg.connect(
    host=host,
    port=port,
    dbname=database,
    user=user,
    password=token,
    sslmode="require"
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL UNIQUE,
    city VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

connection.commit()

print("✅ Users table created successfully!")

cursor.close()
connection.close()