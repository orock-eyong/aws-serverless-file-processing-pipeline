import json
import boto3
import os
from datetime import datetime
from urllib.parse import unquote_plus

# ─── Clients ────────────────────────────────────────────────────
s3       = boto3.client('s3')
sns      = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

# ─── Environment Variables ───────────────────────────────────────
SNS_TOPIC_ARN     = os.environ.get('SNS_TOPIC_ARN')
DDB_TABLE_NAME    = os.environ.get('DDB_TABLE_NAME', 'TextFileMetadata')
DDB_PARTITION_KEY = os.environ.get('DDB_PARTITION_KEY', 'fileName')
PROCESSED_BUCKET  = os.environ.get('PROCESSED_BUCKET')


def process_file(bucket, key):
    """Core processing logic used by both SQS and Step Functions paths."""
    print(f"Processing file: s3://{bucket}/{key}")

    filename      = os.path.basename(key)
    download_path = f'/tmp/{filename}'
    s3.download_file(bucket, key, download_path)

    with open(download_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    word_count = len(text.split())
    print(f"Word count for {key}: {word_count}")

    # Save result to processed bucket
    result_key  = f'wordcount-{filename}'
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
        'bucket':    bucket,
        'key':       key,
        'wordCount': word_count
    }


def lambda_handler(event, context):
    print(f"Raw event received: {json.dumps(event)}")

    # ── Step Functions path ──────────────────────────────────────
    if 'action' in event:
        action = event['action']
        key    = event['key']

        if action == 'move':
            source_bucket      = event['sourceBucket']
            destination_bucket = event['destinationBucket']
            copy_source        = {'Bucket': source_bucket, 'Key': key}
            s3.copy_object(
                CopySource=copy_source,
                Bucket=destination_bucket,
                Key=key
            )
            print(f"Copied {key} from {source_bucket} to {destination_bucket}")
            return {
                'bucket': source_bucket,
                'key':    key
            }
        else:
            bucket = event['bucket']
            return process_file(bucket, key)

    # ── SQS path ─────────────────────────────────────────────────
    if 'Records' in event:
        for sqs_record in event['Records']:
            try:
                sqs_body = json.loads(sqs_record['body'])
                if 'Records' not in sqs_body:
                    continue
                for s3_record in sqs_body['Records']:
                    bucket = s3_record['s3']['bucket']['name']
                    key    = unquote_plus(s3_record['s3']['object']['key'])
                    process_file(bucket, key)
            except Exception as e:
                print(f"ERROR processing record: {str(e)}")
                raise e

    return {'statusCode': 200}
