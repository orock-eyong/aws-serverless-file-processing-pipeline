# V5b - CloudFormation Regional

## Overview
Builds on V5a by making the CloudFormation template fully 
region-aware. Resource names automatically include the AWS region 
so the same template can be deployed in any AWS region without 
naming conflicts.

## What's New in V5b

| Feature | Description |
|---------|-------------|
| Region-aware naming | All resources include AWS region in their names |
| Multi-region support | Same template deploys cleanly in any AWS region |
| Regional S3 endpoint | Presigned URLs use regional endpoint to avoid redirects |
| No naming conflicts | Deploy in eu-north-1 and us-east-1 simultaneously |

## Architecture
Same as V5a but with region-aware resource naming.

## Resource Naming Convention

| V5a Name | V5b Name |
|----------|----------|
| `prod-upload-bucket` | `prod-eu-north-1-upload-bucket` |
| `prod-FileProcessingQueue` | `prod-eu-north-1-FileProcessingQueue` |
| `prod-WordCountProcessor` | `prod-eu-north-1-WordCountProcessor` |
| `prod-FileProcessingWorkflow` | `prod-eu-north-1-FileProcessingWorkflow` |

## Prerequisites

- V5a completed and understood
- Basic understanding of CloudFormation parameters

## Setup Instructions

### Step 1 — Download the Template

1. Download cloudformation/pipeline.yaml
***from this repository***
2. Save it to your computer

### Step 2 — Deploy the Stack

1. Go to AWS Console → CloudFormation
2. Make sure you are in your target region
3. Click "Create stack"
4. Select "With new resources (standard)"
5. Select "Upload a template file"
6. Click "Choose file"
7. Select pipeline.yaml
8. Click "Next"

### Step 3 — Fill in Parameters

Stack name: FileProcessingPipeline

- Parameters:
- Environment: prod
- UploadBucketName: files-upload
- ProcessedBucketName: files-processed
- DynamoDBTableName: FileMetadata
- NotificationEmail: your-email@example.com

***The actual resource names will be:***
- prod-eu-north-1-files-upload ← Upload bucket
- prod-eu-north-1-files-processed ← Processed bucket
- prod-eu-north-1-FileMetadata ← DynamoDB table
- prod-eu-north-1-FileProcessingQueue ← SQS queue
- prod-eu-north-1-WordCountProcessor ← Lambda function (*depending on your region*)

### Step 4 — Configure Stack Options

1. Leave all options as default
2. Scroll down to "Capabilities"
3. Check the checkbox:
***✅ "I acknowledge that AWS CloudFormation***
***might create IAM resources with custom names."***
4. Click "Submit"

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

## Deploying to Multiple Regions

**The same template can be deployed to different regions simultaneously:**

- Region 1: eu-north-1
- Stack name: FileProcessingPipeline
- Resources: prod-eu-north-1-files-upload, etc.

- Region 2: us-east-1
- Stack name: FileProcessingPipeline
- Resources: prod-us-east-1-files-upload, etc.

***No naming conflicts because the region is part of every resource name!**

## CloudFormation Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| Environment | Environment name prefix | prod |
| UploadBucketName | Base name for S3 upload bucket | files-upload |
| ProcessedBucketName | Base name for S3 processed bucket | files-processed |
| DynamoDBTableName | Base name for DynamoDB table | FileMetadata |
| NotificationEmail | Email for notifications | - |

## Outputs

| Output | Description |
|--------|-------------|
| ApiUrl | API Gateway URL for the upload portal |
| UploadBucketName | Full name of the created upload bucket |
| ProcessedBucketName | Full name of the created processed bucket |
| DynamoDBTableName | Full name of the created DynamoDB table |
| StateMachineArn | ARN of the Step Functions state machine |
| Region | AWS region where stack was deployed |

## Cleaning Up

**To delete all resources:**

1. Empty both S3 buckets first
2. Go to CloudFormation console
3. Select "FileProcessingPipeline" stack
4. Click "Delete"
5. Confirm deletion

## Key Differences From V5a

| Aspect | V5a | V5b |
|--------|-----|-----|
| Resource names | `prod-upload-bucket` | `prod-eu-north-1-upload-bucket` |
| S3 endpoint | Global | Regional |
| Multi-region | ❌ May conflict | ✅ No conflicts |
| Complexity | Simpler | Slightly more complex |
