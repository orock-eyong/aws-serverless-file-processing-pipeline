# V5a - CloudFormation Basic
![AWS](https://img.shields.io/badge/AWS-Serverless-orange)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-yellow)
![API Gateway](https://img.shields.io/badge/AWS-API_Gateway-red)
![S3](https://img.shields.io/badge/AWS-S3-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Overview
Builds on V4 by automating the entire infrastructure deployment 
using AWS CloudFormation. Instead of manually creating each 
resource through the AWS Console, a single YAML template creates 
everything automatically in one deployment.

## What's New in V5a

| Feature | Description |
|---------|-------------|
| AWS CloudFormation | Single template deploys entire infrastructure |
| Automated IAM Roles | All roles and policies created automatically |
| Automated Resource Naming | Resources named using Environment parameter |
| Rollback Protection | CloudFormation automatically rolls back on failure |

## Architecture
Same as V4 but fully automated via CloudFormation.

## Services Used

| Service | Purpose |
|---------|---------|
| AWS CloudFormation | Automates infrastructure deployment |
| GitHub Pages | Hosts the file upload portal |
| Amazon API Gateway | REST API for presigned URL generation |
| AWS Lambda - GeneratePresignedUrl | Generates S3 presigned URLs |
| AWS Lambda - SQSTriggerStepFunctions | Starts Step Functions from SQS events |
| AWS Lambda - WordCountProcessor | Handles all processing steps |
| AWS Step Functions | Orchestrates the processing workflow |
| Amazon S3 | Stores uploaded and processed files |
| Amazon SQS | Buffers and decouples S3 events |
| Amazon SQS DLQ | Captures failed processing messages |
| Amazon DynamoDB | Stores file metadata and word counts |
| Amazon SNS | Sends user and owner notifications |
| Amazon CloudWatch | Logs monitoring and DLQ alarms |

## Prerequisites

- V4 completed and working
- AWS CLI installed (optional but helpful)
- Basic understanding of YAML

## Setup Instructions

### Step 1 — Download the Template

1. Download cloudformation/pipeline.yaml
***from this repository***
2. Save it to your computer

### Step 2 — Deploy the Stack

1. Go to AWS Console → CloudFormation
2. Click "Create stack"
3. Select "With new resources (standard)"
4. Select "Upload a template file"
5. Click "Choose file"
6. Select pipeline.yaml
7. Click "Next"

### Step 3 — Fill in Parameters

Stack name: FileProcessingPipeline

Parameters:
- Environment: prod
- UploadBucketName: your-upload-bucket-name
- ProcessedBucketName: your-processed-bucket-name
- DynamoDBTableName: TextFileMetadata
- NotificationEmail: your-email@example.com

### Step 4 — Configure Stack Options

1. Leave all options as default
2. Scroll down to "Capabilities"
3. Check the checkbox:
      ***✅ "I acknowledge that AWS CloudFormation***
            ***might create IAM resources with custom names.***"
5. Click "Submit"

### Step 5 — Wait for Deployment

1. Watch the Events tab
2. Wait for all resources to show CREATE_COMPLETE
3. The full deployment takes 3-5 minutes

### Step 6 — Get the API URL

1. Click on the "Outputs" tab
2. Copy the "ApiUrl" value
3. Update the API_URL in frontend/upload.html
4. Commit the change to GitHub

### Step 7 — Test

1. Go to your GitHub Pages portal
2. Upload a .txt or .pdf file
3. Verify upload succeeds
4. Check Step Functions execution
5. Check DynamoDB for metadata
6. Check email for notification

## CloudFormation Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| Environment | Environment name prefix | prod |
| UploadBucketName | Name of S3 upload bucket | upload-bucket |
| ProcessedBucketName | Name of S3 processed bucket | processed-bucket |
| DynamoDBTableName | Name of DynamoDB table | FileMetadata |
| NotificationEmail | Email for notifications | - |

## Outputs

| Output | Description |
|--------|-------------|
| ApiUrl | API Gateway URL for the upload portal |
| UploadBucketName | Name of the created upload bucket |
| ProcessedBucketName | Name of the created processed bucket |
| DynamoDBTableName | Name of the created DynamoDB table |
| StateMachineArn | ARN of the Step Functions state machine |

## Cleaning Up

**To delete all resources created by this stack:**

1. Go to CloudFormation console
2. Select "FileProcessingPipeline" stack
3. Click "Delete"
4. Confirm deletion

#### ⚠️ Note: S3 buckets must be emptied before the stack can be deleted. ⚠️

## What's Next

Move to [V5b - CloudFormation Regional](../v5b-cloudformation-regional/)
to make the template region-aware so it can be deployed 
in any AWS region without naming conflicts.

