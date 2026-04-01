# V4 - Step Functions
![AWS](https://img.shields.io/badge/AWS-Serverless-orange)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-yellow)
![API Gateway](https://img.shields.io/badge/AWS-API_Gateway-red)
![S3](https://img.shields.io/badge/AWS-S3-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Overview
Builds on V3 by adding AWS Step Functions to orchestrate the file 
processing workflow. Instead of Lambda directly processing files 
triggered by SQS, a bridge Lambda starts a Step Functions state 
machine that coordinates each processing step with proper error 
handling and retries.

## What's New in V4

| Feature | Description |
|---------|-------------|
| AWS Step Functions | Orchestrates the processing workflow |
| Lambda - SQSTriggerStepFunctions | Bridge Lambda that starts Step Functions from SQS |
| Workflow States | ValidateFile, ProcessWordCount, StoreMetadata, MoveToProcessedBucket, NotifyUser, HandleError |
| Error Handling | Automatic retries and error notification via SNS |

## Architecture

User → GitHub Pages Portal → API Gateway → Lambda (GeneratePresignedUrl)
↓
S3 Presigned URL
↓
User → PUT file directly to S3
↓
SQS Queue
↓
Lambda (SQSTriggerStepFunctions)
↓
Step Functions State Machine
↓
┌───────────────────────────┐
│ 1. ValidateFile │
│ 2. ProcessWordCount │
│ 3. StoreMetadata │
│ 4. MoveToProcessedBucket │
│ 5. NotifyUser → SNS │
└───────────────────────────┘
↓
HandleError → SNS (on any failure)

## Services Used

| Service | Purpose |
|---------|---------|
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

- V3 completed and working
- Existing S3 buckets, DynamoDB table, SNS topics and SQS queues from V3

## Setup Instructions

### Step 1 — Create SQSTriggerStepFunctions Lambda

1. Go to AWS Console → Lambda
2. Click "Create function"
3. Select "Author from scratch"
4. Function name: SQSTriggerStepFunctions
5. Runtime: Python 3.12
6. Execution role: Create new role with basic Lambda permissions
7. Click "Create function"
8. Paste code from lambda/sqs_trigger_step_functions.py
9. Click "Deploy"

### Step 2 — Create Step Functions State Machine

1. Go to AWS Console → Step Functions
2. Click "Create state machine"
3. Name: FileProcessingWorkflow
4. Type: Standard
5. Click "Create"
6. Click "Edit" on the state machine
7. Switch to "Code" view
8. Replace the code with the content from
***step-functions/state-machine-definition.json***
9. Click "Save"

### Step 3 — Add Environment Variable to SQSTriggerStepFunctions

1. Go to Lambda console
2. Click on "SQSTriggerStepFunctions"
3. Click "Configuration" tab
4. Click "Environment variables"
5. Click "Edit"
6. Add:
***STATE_MACHINE_ARN = your-state-machine-arn***
7. Click "Save"

### Step 4 — Apply IAM Least Privilege

#### SQSTriggerStepFunctions Lambda Role

1. Go to IAM → Roles
2. Find the role for SQSTriggerStepFunctions Lambda
3. Add inline policy from:
***policies/sqs-trigger-role-policy.json***

#### Step Functions Role
*Step Functions automatically creates a role during setup.*
*Verify it has permissions from:*
***policies/step-functions-role-policy.json***

### Step 5 — Remove Old SQS Trigger from WordCount Lambda

1. Go to Lambda console
2. Click on "WordCountProcessor"
3. Click "Configuration" tab
4. Click "Triggers"
5. Select the SQS trigger
6. Click "Remove"
7. Confirm removal

### Step 6 — Add SQS Trigger to SQSTriggerStepFunctions

1. Go to Lambda console
2. Click on "SQSTriggerStepFunctions"
3. Click "Add trigger"
4. Select "SQS"
5. SQS queue: FileProcessingQueue
6. Batch size: 1
7. Click "Add"

### Step 7 — Update WordCount Lambda Code

1. Go to Lambda console
2. Click on "WordCountProcessor"
3. Replace the code with content from
***lambda/word_count_processor.py***
4. Click "Deploy"

### Step 8 — Test

1. Go to your GitHub Pages portal
2. Upload a .txt or .pdf file
3. Go to Step Functions console
4. Click on "FileProcessingWorkflow"
5. Click on "Executions" tab
6. Verify all states are green
7. Check DynamoDB for metadata entry
8. Check email for notification

## State Machine Flow

flowchart TD
A[Start] --> B[ValidateFile]
B -->|Success| C[ProcessWordCount]
B -->|Error| G[HandleError]
C -->|Success| D[StoreMetadata]
C -->|Error| G
D -->|Success| E[MoveToProcessedBucket]
D -->|Error| G
E -->|Success| F[NotifyUser]
E -->|Error| G
F --> H[SuccessEnd]
G --> I[FailEnd]

## Expected Results

| Check | Expected |
|-------|----------|
| Step Functions Execution | All states green |
| S3 Upload Bucket | File present |
| S3 Processed Bucket | wordcount-filename.txt present |
| DynamoDB | New metadata entry |
| Email | Success notification received |

## IAM Least Privilege Summary

| Component | Permissions |
|-----------|-------------|
| GeneratePresignedUrl Lambda | s3:PutObject on upload bucket only |
| SQSTriggerStepFunctions Lambda | sqs:ReceiveMessage/DeleteMessage/GetQueueAttributes, states:StartExecution |
| WordCount Lambda | s3:GetObject, s3:PutObject, s3:CopyObject, dynamodb:PutItem, sns:Publish, sqs permissions |
| Step Functions | lambda:InvokeFunction, sns:Publish |

## What's Next

Move to [V5a - CloudFormation Basic](../v5a-cloudformation-basic/)
to automate the entire infrastructure deployment with CloudFormation.

