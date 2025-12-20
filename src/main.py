from flask import Flask, request, render_template
import boto3
import uuid
import json
import mysql.connector

import os

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-2')
S3_BUCKET = os.environ.get('S3_BUCKET', 'filesharebucket90')
LAMBDA_NAME = os.environ.get('LAMBDA_NAME', 'SendEmailWithSES')

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME', 'filesharing')

app = Flask(__name__)

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# index
@app.route('/')
def index():
    return render_template('index.html')

# upload
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    email_input = request.form.get('emails', '')
    email_list = [e.strip() for e in email_input.split(',') if e.strip()]

    if not file:
        return "Please upload a file."
    if not email_list:
        return "Please enter at least one email address."
    if len(email_list) > 5:
        return "Maximum of 5 email addresses allowed."

    try:
        file_id = str(uuid.uuid4())
        s3_key = f"uploads/{file_id}_{file.filename}"
        s3_client.upload_fileobj(file, S3_BUCKET, s3_key)

        file_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': s3_key},
            ExpiresIn=86400
        )

        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO uploads (id, filename, s3_key, download_url, email_list)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            file_id,
            file.filename,
            s3_key,
            file_url,
            ','.join(email_list)
        ))

        conn.commit()
        cursor.close()
        conn.close()
        print("RDS Logging the timestamps Successful")

        lambda_payload = {
            "links": [{"recipient": email, "url": file_url} for email in email_list],
            "filename": file.filename
        }

        lambda_client.invoke(
            FunctionName=LAMBDA_NAME,
            InvocationType='Event',
            Payload=json.dumps(lambda_payload)
        )

        return f"""
            File uploaded and email(s) sent to: {', '.join(email_list)}<br><br>
            Recipients can now access the file through the provided links in the email.
        """

    except Exception as e:
        return f"Uploading the file failed: {str(e)}"

# main
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
