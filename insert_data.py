import re

import boto3
import psycopg

host = "codealpha-data-redundancy-removal-system.cluster-czqok2wc0j7j.ap-south-1.rds.amazonaws.com"
port = 5432
database = "postgres"
user = "postgres"
region = "ap-south-1"


def get_connection():
    rds = boto3.client("rds", region_name=region)

    token = rds.generate_db_auth_token(
        DBHostname=host,
        Port=port,
        DBUsername=user,
        Region=region
    )

    return psycopg.connect(
        host=host,
        port=port,
        dbname=database,
        user=user,
        password=token,
        sslmode="require"
    )


def validate_data(name, email, phone, city):

    if not name or not city:
        return False, "Required field is missing"

    # Email validation
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(email_pattern, email):
        return False, "Invalid email"

    # Phone validation
    if not phone.isdigit() or len(phone) != 10:
        return False, "Invalid phone number"

    return True, "Valid"


def add_user(name, email, phone, city):

    # 1. Validate email and phone
    valid, message = validate_data(
        name,
        email,
        phone,
        city
    )

    if not valid:
        print("❌ INVALID DATA DETECTED")
        print("Reason:", message)
        return

    connection = get_connection()
    cursor = connection.cursor()

    # 2. Duplicate detection
    cursor.execute(
        """
        SELECT id, name, email, phone, city
        FROM users
        WHERE email = %s OR phone = %s
        """,
        (email.lower(), phone)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        print("❌ DUPLICATE DATA DETECTED")
        print("Existing record:", existing_user)

        cursor.close()
        connection.close()
        return

    # 3. Insert verified unique data
    cursor.execute(
        """
        INSERT INTO users (name, email, phone, city)
        VALUES (%s, %s, %s, %s)
        """,
        (name, email.lower(), phone, city)
    )

    connection.commit()

    print("✅ DATA VERIFIED AND ADDED SUCCESSFULLY")

    cursor.close()
    connection.close()


# -----------------------------
# USER INPUT
# -----------------------------

print("\n===== DATA REDUNDANCY REMOVAL SYSTEM =====\n")

name = input("Enter name: ")
email = input("Enter email: ")
phone = input("Enter phone number: ")
city = input("Enter city: ")

add_user(name, email, phone, city)