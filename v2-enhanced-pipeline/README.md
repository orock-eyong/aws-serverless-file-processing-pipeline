# V2 - Enhanced Pipeline

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

Go to AWS Console → SQS
Click "Create queue"
Type: Standard
Name: FileProcessingQueue
Visibility timeout: 300 seconds
Under "Dead-letter queue":
Enable dead-letter queue: ✅
Choose queue: FileProcessingDLQ
Maximum receives: 3
Click "Create queue"
Copy the Queue ARN for later
