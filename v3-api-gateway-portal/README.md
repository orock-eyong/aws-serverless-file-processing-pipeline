# V3 - API Gateway & Upload Portal
![AWS](https://img.shields.io/badge/AWS-Serverless-orange)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-yellow)
![API Gateway](https://img.shields.io/badge/AWS-API_Gateway-red)
![S3](https://img.shields.io/badge/AWS-S3-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Overview
Builds on V2 by adding a web-based file upload portal hosted on 
GitHub Pages, an API Gateway to handle upload requests securely,
and IAM Least Privilege to lock down all permissions to only what
each service needs.

## What's New in V3

| Feature | Description |
|---------|-------------|
| GitHub Pages Portal | Web interface for file uploads |
| Amazon API Gateway | Secure REST API for presigned URL generation |
| AWS Lambda (GeneratePresignedUrl) | Generates secure S3 upload URLs |
| IAM Least Privilege | Each component has minimum required permissions only |

## Architecture

User → GitHub Pages Portal → API Gateway → Lambda (GeneratePresignedUrl)
↓
S3 Presigned URL
↓
User → PUT file directly to S3 → SQS → Lambda (WordCount)
↓
DynamoDB + SNS + S3 Processed

## Services Used

| Service | Purpose |
|---------|---------|
| GitHub Pages | Hosts the file upload portal |
| Amazon API Gateway | REST API for presigned URL generation |
| AWS Lambda - GeneratePresignedUrl | Generates S3 presigned URLs |
| AWS Lambda - WordCountProcessor | Processes files and counts words |
| Amazon S3 | Stores uploaded and processed files |
| Amazon SQS | Buffers and decouples S3 events |
| Amazon SQS DLQ | Captures failed processing messages |
| Amazon DynamoDB | Stores file metadata and word counts |
| Amazon SNS | Sends user and owner notifications |
| Amazon CloudWatch | Logs monitoring and DLQ alarms |

## Prerequisites

- V2 completed and working
- GitHub account for hosting the portal
- Existing S3 buckets, DynamoDB table and SNS topics from V2

## Setup Instructions

### Step 1 — Create GeneratePresignedUrl Lambda

1. Go to AWS Console → Lambda
2. Click "Create function"
3. Select "Author from scratch"
4. Function name: GeneratePresignedUrl
5. Runtime: Python 3.12
6. Execution role: Create new role with basic Lambda permissions
7. Click "Create function"
8. Paste code from lambda/generate_presigned_url.py
9. Click "Deploy"

**Add environment variables:**
BUCKET_NAME = your-upload-bucket-name
CORS_ALLOW_ORIGIN = https://your-github-username.github.io
ALLOWED_EXTENSIONS = .txt,.csv,.doc,.pdf

### Step 2 — Apply IAM Least Privilege

#### GeneratePresignedUrl Lambda Role

1. Go to IAM → Roles
2. Find the role for GeneratePresignedUrl Lambda
3. Remove any broad policies
4. Add inline policy from:
**policies/generate-presigned-url-role-policy.json**

#### WordCount Lambda Role

1. Go to IAM → Roles
2. Find the role for WordCount Lambda
3. Remove these broad policies:
- AmazonS3FullAccess
- AmazonSNSFullAccess
- AmazonSQSFullAccess
- AmazonDynamoDBFullAccess
4. Add inline policy from:
**policies/word-count-processor-role-policy.json**

### Step 3 — Create API Gateway

1. Go to AWS Console → API Gateway
2. Click "Create API"
3. Select "REST API"
4. Click "Build"
5. API name: FileUploadApi
6. Click "Create API"

**Create /upload resource:**
1. Click "Actions" → "Create Resource"
2. Resource name: upload
3. Resource path: /upload
4. Click "Create Resource"

**Create POST method:**
1. Click "Actions" → "Create Method"
2. Select "POST"
3. Integration type: Lambda Function
4. Lambda Proxy Integration: ✅ Enabled
5. Lambda function: GeneratePresignedUrl
6. Click "Save"

**Configure CORS:**
1. Select /upload resource
2. Click "Actions" → "Enable CORS"
3. Access-Control-Allow-Origin: *
4. Click "Enable CORS and replace existing headers"

**Deploy API:**
1. Click "Actions" → "Deploy API"
2. Stage: prod
3. Click "Deploy"
4. Copy the API URL from the stage editor

### Step 4 — Set Up GitHub Pages Portal

1. Create a new GitHub repository
- Name: your-github-username.github.io
- OR use an existing repository
2. Create a new file: file-upload-portal/index.html
3. Paste code from frontend/upload.html
4. Replace API_URL with your API Gateway URL
5. Commit the file
6. Go to repository Settings
7. Click "Pages"
8. Source: Deploy from branch
9. Branch: main
10. Click "Save"

### Step 5 — Test

1. Go to your GitHub Pages URL
2. Upload a .txt or .pdf file
3. Check browser console for success
4. Check S3 upload bucket for file
5. Check DynamoDB for metadata entry
6. Check email for notification

## Expected Results

| Check | Expected |
|-------|----------|
| Browser Console | Upload successful message |
| S3 Upload Bucket | File present |
| S3 Processed Bucket | wordcount-filename.txt present |
| DynamoDB | New metadata entry |
| Email | Success notification received |

## IAM Least Privilege Summary

| Component | Permissions |
|-----------|-------------|
| GeneratePresignedUrl Lambda | s3:PutObject on upload bucket only |
| WordCount Lambda | s3:GetObject on upload bucket, s3:PutObject on processed bucket, dynamodb:PutItem on specific table, sns:Publish on specific topic, sqs:ReceiveMessage/DeleteMessage/GetQueueAttributes on specific queue |

## What's Next

Move to [V4 - Step Functions](../v4-step-functions/)
to add workflow orchestration with AWS Step Functions.


