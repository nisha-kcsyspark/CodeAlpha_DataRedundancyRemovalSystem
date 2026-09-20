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
    sslmode="require",
    connect_timeout=10
)

print("✅ AWS Aurora PostgreSQL Connected Successfully!")

cursor = connection.cursor()

cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS unique_user_email
    ON users (email);
""")

cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS unique_user_phone
    ON users (phone);
""")

connection.commit()

print("Email and phone duplicate protection added successfully!")

cursor.close()
connection.close()