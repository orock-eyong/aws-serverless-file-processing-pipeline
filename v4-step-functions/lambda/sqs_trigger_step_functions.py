import json
import boto3
import os
from urllib.parse import unquote_plus

stepfunctions = boto3.client('stepfunctions')

# ─── Environment Variables ───────────────────────────────────────
STATE_MACHINE_ARN = os.environ.get('STATE_MACHINE_ARN')


def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")

    for record in event['Records']:
        # Parse SQS message body
        body    = json.loads(record['body'])
        s3_event = body['Records'][0]['s3']

        # Extract bucket and key
        bucket = s3_event['bucket']['name']
        key    = unquote_plus(s3_event['object']['key'])

        print(f"Starting Step Functions for: {bucket}/{key}")

        # Start Step Functions execution
        response = stepfunctions.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            input=json.dumps({
                'action': 'validate',
                'bucket': bucket,
                'key':    key
            })
        )

        print(f"Execution started: {response['executionArn']}")

    return {'statusCode': 200}
