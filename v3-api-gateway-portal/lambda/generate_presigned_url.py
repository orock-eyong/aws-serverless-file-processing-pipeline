import json
import boto3
import os
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

# ─── Environment Variables ───────────────────────────────────────
BUCKET_NAME        = os.environ.get('BUCKET_NAME')
ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS', '.txt,.csv,.doc,.pdf').split(',')
ALLOWED_ORIGINS    = os.environ.get('CORS_ALLOW_ORIGIN', '*').split(',')


def get_cors_headers(event):
    origin = event.get('headers', {}).get('origin') or \
             event.get('headers', {}).get('Origin', '')
    allowed_origin = origin if origin in ALLOWED_ORIGINS else ALLOWED_ORIGINS[0]
    return {
        'Access-Control-Allow-Origin':  allowed_origin,
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'POST,OPTIONS',
        'Vary': 'Origin'
    }


def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    CORS_HEADERS = get_cors_headers(event)

    # ── Handle OPTIONS preflight ──────────────────────────────────
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps('OK')
        }

    try:
        body         = json.loads(event['body'])
        filename     = body.get('filename')
        content_type = body.get('contentType', 'application/octet-stream')

        if not filename:
            return {
                'statusCode': 400,
                'headers': CORS_HEADERS,
                'body': json.dumps({'error': 'filename is required'})
            }

        if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            return {
                'statusCode': 400,
                'headers': CORS_HEADERS,
                'body': json.dumps({
                    'error': f'Invalid file type. Allowed: {ALLOWED_EXTENSIONS}'
                })
            }

        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket':      BUCKET_NAME,
                'Key':         filename,
                'ContentType': content_type
            },
            ExpiresIn=300
        )

        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps({
                'upload_url': presigned_url,
                'filename':   filename,
                'expires_in': '5 minutes'
            })
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': str(e)})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': 'An unexpected error occurred'})
        }
