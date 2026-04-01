# V2 - Enhanced Pipeline
![AWS](https://img.shields.io/badge/AWS-Serverless-orange)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Architecture](https://img.shields.io/badge/Architecture-Event--Driven-green)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

## Overview
Builds on V1 by adding SQS for decoupled processing, a Dead Letter 
Queue (DLQ) for failed messages and a CloudWatch Alarm to alert 
the owner when messages land in the DLQ.

## What's New in V2

| Feature | Description |
|---------|-------------|
| Amazon SQS | Decouples S3 events from Lambda processing |
| SQS Dead Letter Queue | Captures messages that fail after 3 retries |
| CloudWatch Alarm | Monitors DLQ and alerts owner via SNS |

## Architecture
User → S3 (Upload) → SQS Queue → Lambda → DynamoDB (Metadata)
→ SNS (User Notification)
→ S3 (Processed Bucket)
↓
DLQ (Failed Messages)
↓
CloudWatch Alarm
↓
SNS (Owner Alert)

<p align="center">
  <img src="v2-architecture.png" width="700">
</p>

## Services Used

| Service | Purpose |
|---------|---------|
| Amazon S3 | Stores uploaded and processed files |
| Amazon SQS | Buffers and decouples S3 events |
| Amazon SQS DLQ | Captures failed processing messages |
| AWS Lambda | Processes files and counts words |
| Amazon DynamoDB | Stores file metadata and word counts |
| Amazon SNS | Sends user and owner notifications |
| Amazon CloudWatch | Logs, monitoring and DLQ alarms |

## Prerequisites

- V1 completed and working
- Existing S3 upload and processed buckets
- Existing DynamoDB table
- Existing SNS topic for user notifications

## Setup Instructions

### Step 1 — Create Owner Alert SNS Topic

1. Go to AWS Console → SNS
2. Click "Create topic"
3. Type: Standard
4. Name: OwnerAlertTopic
5. Click "Create topic"
6. Click "Create subscription"
7. Protocol: Email
8. Endpoint: your-email@example.com
9. Click "Create subscription"
10. Confirm subscription from your email

### Step 2 — Create Dead Letter Queue

1. Go to AWS Console → SQS
2. Click "Create queue"
3. Type: Standard
4. Name: FileProcessingDLQ
5. Message retention period: 14 days
6. Click "Create queue"
7. Copy the DLQ ARN for later
 
### Step 3 — Create Main SQS Queue

1. Go to AWS Console → SQS
2. Click "Create queue"
3. Type: Standard
4. Name: FileProcessingQueue
5. Visibility timeout: 300 seconds
6. Under "Dead-letter queue":
- *Enable dead-letter queue:* ✅
- *Choose queue: FileProcessingDLQ*
- *Maximum receives: 3*
7. Click "Create queue"
8. Copy the Queue ARN for later

### Step 4 — Allow S3 to Send Messages to SQS

1. Click on "FileProcessingQueue"
2. Click "Access policy" tab
3. Click "Edit"
4. Paste the policy from
**policies/sqs-queue-policy.json**
5. Replace YOUR-QUEUE-ARN and
**YOUR-BUCKET-NAME with your values**
6. Click "Save"

### Step 5 — Connect S3 to SQS

1. Go to your S3 upload bucket
2. Click "Properties" tab
3. Scroll to "Event notifications"
4. Click "Create event notification"
5. Event name: SendToSQS
6. Event type: s3:ObjectCreated:*
7. Destination: SQS queue
8. SQS queue: FileProcessingQueue
9. Click "Save changes"

### Step 6 — Update Lambda Trigger

1. Go to Lambda console
2. Click on your V1 Lambda function
**or create a new one named: v2-text-word-count**
3. Remove the S3 trigger if present
4. Click "Add trigger"
5. Select "SQS"
6. SQS queue: FileProcessingQueue
7. Batch size: 1
8. Click "Add"

### Step 7 — Update Lambda Code

1. Replace the Lambda code with
**the code from lambda/lambda_function.py**
2. Click "Deploy"

### Step 8 — Update IAM Role

1. Go to IAM → Roles
2. Click on your Lambda role
3. Remove old broad policies
4. Add inline policy from
**policies/lambda-role-policy.json**

### Step 9 — Create CloudWatch Alarm

1. Go to AWS Console → CloudWatch
2. Click "Alarms" → "Create alarm"
3. Click "Select metric"
4. Search for "SQS" → "Queue metrics"
5. Find "FileProcessingDLQ"
6. Select "ApproximateNumberOfMessagesVisible"
7. Click "Select metric"
8. Conditions:
- Threshold type: Static
- Whenever value is: Greater/Equal
- Than: 1
9. Click "Next"
10. Notification:
- Select "In alarm"
- SNS topic: OwnerAlertTopic
11. Click "Next"
12. Alarm name: DLQAlarm
13. Click "Create alarm"
  
### Step 10 — Test

1. Upload a .txt file to S3
2. Check SQS queue message count
3. Check Lambda CloudWatch logs
4. Check DynamoDB for new entry
5. Check email for notification

## Expected Results

| Check | Expected |
|-------|----------|
| SQS Queue | Message received and processed |
| CloudWatch Logs | Processing logs visible |
| DynamoDB | New item with fileName and wordCount |
| Email | Success notification received |
| DLQ | Empty (no failed messages) |

## What's Next

Move to [V3 - API Gateway & Upload Portal](../v3-api-gateway-portal/)
to add a web upload interface and API Gateway.
