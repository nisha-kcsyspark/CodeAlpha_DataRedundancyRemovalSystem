import re

import boto3
import psycopg
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

HOST = "codealpha-data-redundancy-removal-system.cluster-czqok2wc0j7j.ap-south-1.rds.amazonaws.com"
PORT = 5432
DATABASE = "postgres"
USER = "postgres"
REGION = "ap-south-1"


def get_connection():

    rds = boto3.client("rds", region_name=REGION)

    token = rds.generate_db_auth_token(
        DBHostname=HOST,
        Port=PORT,
        DBUsername=USER,
        Region=REGION
    )

    return psycopg.connect(
        host=HOST,
        port=PORT,
        dbname=DATABASE,
        user=USER,
        password=token,
        sslmode="require",
        connect_timeout=5
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add_user():

    name = request.form["name"].strip()
    email = request.form["email"].strip().lower()
    phone = request.form["phone"].strip()
    city = request.form["city"].strip()

    # 1. Required fields
    if not name or not email or not phone or not city:
        flash("Invalid Data: All fields are required!", "error")
        return redirect(url_for("home"))

    # 2. Email validation
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(email_pattern, email):
        flash("Invalid Email Detected!", "error")
        return redirect(url_for("home"))

    # 3. Phone validation
    if not phone.isdigit() or len(phone) != 10:
        flash("Invalid Phone Number Detected!", "error")
        return redirect(url_for("home"))

    connection = get_connection()
    cursor = connection.cursor()

    # 4. Duplicate detection
    cursor.execute(
        """
        SELECT id, name, email, phone, city
        FROM users
        WHERE email = %s OR phone = %s
        """,
        (email, phone)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        connection.close()

        flash("Duplicate Data Detected!", "error")
        return redirect(url_for("home"))

    # 5. Insert verified unique data
    cursor.execute(
        """
        INSERT INTO users (name, email, phone, city)
        VALUES (%s, %s, %s, %s)
        """,
        (name, email, phone, city)
    )

    connection.commit()

    cursor.close()
    connection.close()

    flash("Data Verified and Added Successfully!", "success")

    return redirect(url_for("home"))


@app.route("/records")
def records():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, email, phone, city, created_at
        FROM users
        ORDER BY id DESC
        """
    )

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("records.html", users=users)


if __name__ == "__main__":
    app.run(debug=True)