# Secure File-Sharing Web Application on AWS

**Secure, Scalable, and Serverless.**

## Overview
This project is a secure file-sharing web application architected on AWS. It uses **Python Flask** on **EC2** for the backend, **S3** for scalable file storage, **RDS (MySQL)** for metadata management, and **AWS Lambda/SES** for a decoupled, serverless notification system.

## Key Features
*   **Scalable Compute**: Deployed on AWS EC2 with Auto Scaling potential.
*   **Secure Storage**: Uses AWS S3 for object storage with presigned URLs (optional/future).
*   **Managed Database**: AWS RDS (MySQL) for robust data integrity.
*   **Serverless Notifications**: Decoupled architecture using AWS Lambda triggered by S3 events (or API) to send emails via SES.
*   **Security**: Implemented IAM Roles and Security Groups for least-privilege access.

## Architecture
- **Frontend**: HTML/CSS (Jinja2 Templates).
- **Backend**: Python Flask.
- **Database**: AWS RDS (MySQL).
- **Storage**: AWS S3.
- **Async Tasks**: AWS Lambda + SES.

## Installation
1.  Clone the repo:
    ```bash
    git clone https://github.com/potlurisravanth-png/secure-file-sharing-webapp.git
    cd secure-file-sharing-webapp
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configure Environment Variables (`.env`):
    ```
    DB_HOST=your-rds-endpoint
    DB_USER=admin
    DB_PASSWORD=secret
    S3_BUCKET=your-bucket-name
    ```
4.  Run the app:
    ```bash
    python src/main.py
    ```

## Requirements
*   Python 3.8+
*   Flask
*   Boto3
*   PyMySQL
