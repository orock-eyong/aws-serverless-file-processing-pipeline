import json
import boto3
import os
from datetime import datetime

# ─── Clients ────────────────────────────────────────────────────
s3       = boto3.client('s3')
sns      = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

# ─── Environment Variables ───────────────────────────────────────
SNS_TOPIC_ARN     = os.environ.get('SNS_TOPIC_ARN')
DDB_TABLE_NAME    = os.environ.get('DDB_TABLE_NAME', 'TextFileMetadata')
DDB_PARTITION_KEY = os.environ.get('DDB_PARTITION_KEY', 'fileName')
PROCESSED_BUCKET  = os.environ.get('PROCESSED_BUCKET')

def lambda_handler(event, context):
    try:
        # Get bucket and file info from S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key    = event['Records'][0]['s3']['object']['key']
        print(f"Processing file: s3://{bucket}/{key}")

        # Download file to /tmp
        download_path = f'/tmp/{key}'
        s3.download_file(bucket, key, download_path)

        # Count words
        with open(download_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        word_count = len(text.split())
        print(f"Word count for {key}: {word_count}")

        # Save result to processed bucket
        result_key  = f'wordcount-{key}'
        result_body = f'Total words in {key}: {word_count}'
        s3.put_object(
            Bucket=PROCESSED_BUCKET,
            Key=result_key,
            Body=result_body
        )
        print(f"Result saved to {PROCESSED_BUCKET}/{result_key}")

        # Save metadata to DynamoDB
        table = dynamodb.Table(DDB_TABLE_NAME)
        table.put_item(
            Item={
                DDB_PARTITION_KEY: key,
                'WordCount':       word_count,
                'ProcessedAt':     datetime.utcnow().isoformat()
            }
        )
        print(f"Metadata saved to DynamoDB for {key}")

        # Publish SNS notification
        message = f'File {key} processed successfully! {word_count} words counted.'
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject='Text Processing Complete'
        )
        print(f"SNS notification sent for {key}")

        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }

    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return {
            'statusCode': 500,
            'body': str(e)
        }
