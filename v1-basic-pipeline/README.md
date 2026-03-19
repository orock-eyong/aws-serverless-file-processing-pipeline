# V1 - Basic Pipeline

## Overview
The foundation of the pipeline. A file uploaded to S3 
automatically triggers a Lambda function that counts words, 
stores metadata in DynamoDB and sends an email notification via SNS.

## Architecture

## Services Used

| Service | Purpose |
|---------|---------|
| Amazon S3 | Stores uploaded text files |
| AWS Lambda | Processes files and counts words |
| Amazon DynamoDB | Stores file metadata and word counts |
| Amazon SNS | Sends email notifications |
| Amazon CloudWatch | Logs and monitoring |

## Prerequisites

- AWS Account with console access
- Basic understanding of AWS Console navigation

## Setup Instructions

### Step 1 — Create S3 Bucket

### Step 2 — Create DynamoDB Table

### Step 3 — Create SNS Topic

### Step 4 — Create IAM Role for Lambda

Then add an inline policy:

### Step 5 — Create Lambda Function

Then add the code:

Then add environment variables:

### Step 6 — Connect S3 to Lambda

### Step 7 — Test

## Expected Results

| Check | Expected |
|-------|----------|
| CloudWatch Logs | Processing logs visible |
| DynamoDB | New item with fileName and wordCount |
| Email | Notification received |

## What's Next

Move to [V2 - Enhanced Pipeline](../v2-enhanced-pipeline/) 
to add SQS decoupling and a Dead Letter Queue.
