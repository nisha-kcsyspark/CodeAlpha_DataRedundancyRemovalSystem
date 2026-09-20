# Data Redundancy Removal System

## Project Overview

The Data Redundancy Removal System is a Flask-based web application that validates user data before storing it in an AWS Aurora PostgreSQL database.

The system detects invalid email addresses, invalid phone numbers, and duplicate user data before insertion.

## Objectives

- Validate user input
- Detect invalid email addresses
- Detect invalid phone numbers
- Detect duplicate email addresses
- Detect duplicate phone numbers
- Prevent invalid and duplicate records from being stored
- Store verified unique records in AWS Aurora PostgreSQL
- Provide a user-friendly web interface

## Technology Stack

- Python
- Flask
- PostgreSQL
- AWS Aurora PostgreSQL
- AWS IAM Database Authentication
- Boto3
- Psycopg
- HTML
- CSS
- JavaScript

## System Flow

User Input
↓
Email Validation
↓
Phone Validation
↓
Duplicate Detection
↓
Database Validation
↓
AWS Aurora PostgreSQL
↓
Success / Error Result

## Validation Rules

### Email Validation

The system checks whether the entered email follows a valid email format.

Invalid example:

    testgmail.com

Result:

    Invalid Email Detected!

### Phone Validation

The system accepts a 10-digit numeric phone number.

Invalid example:

    12345

Result:

    Invalid Phone Number Detected!

### Duplicate Detection

The system checks the existing database using email and phone number.

If an existing email or phone number is found:

    Duplicate Data Detected!

The record is not inserted.

## Database Protection

Unique database indexes are implemented for:

- Email
- Phone number

This provides an additional database-level protection against duplicate records.

## AWS Database

The application uses:

- AWS Aurora PostgreSQL
- Port: 5432
- AWS IAM Database Authentication
- SSL connection

AWS credentials are not hard-coded in the application.

## Project Structure

    CodeAlpha_DataRedundancyRemovalSystem/
    │
    ├── app.py
    ├── test_aws.py
    ├── insert_data.py
    ├── requirements.txt
    ├── README.md
    │
    └── templates/
        ├── index.html
        └── records.html

## Installation

Create and activate a Python virtual environment.

Install dependencies:

    pip install -r requirements.txt

## Run Application

Start the Flask application:

    python app.py

Open the application in a browser:

    http://127.0.0.1:5000

## Test Cases

| Test | Input | Expected Result |
|---|---|---|
| Valid data | Unique email and phone | Data Added Successfully |
| Duplicate email | Existing email | Duplicate Data Detected |
| Duplicate phone | Existing phone | Duplicate Data Detected |
| Invalid email | Incorrect email format | Invalid Email Detected |
| Invalid phone | Invalid phone format | Invalid Phone Number Detected |

## Result

The system successfully validates incoming user data, detects invalid and redundant information, and stores only verified unique records in AWS Aurora PostgreSQL.