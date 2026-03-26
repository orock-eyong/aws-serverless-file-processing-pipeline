# AWS Serverless File Processing Pipeline

![AWS](https://img.shields.io/badge/AWS-Serverless-orange)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-yellow)
![API Gateway](https://img.shields.io/badge/AWS-API_Gateway-red)
![S3](https://img.shields.io/badge/AWS-S3-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A step-by-step serverless file processing pipeline built on AWS, 
progressing from a basic Lambda function to a fully automated 
regional CloudFormation infrastructure.

## Pipeline Versions

| Version | Description | Services Added |
|---------|-------------|----------------|
| [V1 - Basic Pipeline](./v1-basic-pipeline/) | Core text processing | S3, Lambda, DynamoDB, SNS, CloudWatch |
| [V2 - Enhanced Pipeline](./v2-enhanced-pipeline/) | Decoupled processing | SQS, DLQ, CloudWatch Alarms |
| [V3 - API Gateway & Upload Portal](./v3-api-gateway-portal/) | Web upload interface | API Gateway, IAM Least Privilege |
| [V4 - Step Functions](./v4-step-functions/) | Orchestrated workflow | Step Functions, SQS Trigger Lambda |
| [V5a - CloudFormation Basic](./v5a-cloudformation-basic/) | Infrastructure as Code | CloudFormation |
| [V5b - CloudFormation Regional](./v5b-cloudformation-regional/) | Region-aware deployment | CloudFormation with region naming |

## 🚀 Quick Start

Choose how you want to explore the project:

### 🔹 Learn Step-by-Step (Recommended)
Start from the basics and build up your understanding:

➡️ Begin with **[V1](./v1-basic-pipeline/) - Basic Pipeline** and progress through each version

### ⚡ Deploy the Full Solution (Fastest)
Deploy the complete architecture in one go:

➡️ Use **[V5b](./v5b-cloudformation-regional/) - CloudFormation Regional Template**

### 🔍 Explore a Specific Version
Jump directly to any stage of the pipeline:

- **V1** — Basic event-driven pipeline  
- **V2** — SQS, DLQ, and fault tolerance  
- **V3** — API Gateway + upload portal  
- **V4** — Step Functions orchestration  
- **V5** — Infrastructure as Code  

Each version folder contains:

- `README.md` — Step-by-step instructions  
- `lambda/` — Function code  
- `policies/` — IAM configurations  
- `frontend/` — Upload UI (V3+)  
- `cloudformation/` — Templates (V5)  

## Quick Start

| I want to... | Go to... |
|---|---|
| Learn step by step | Start with [V1](./v1-basic-pipeline/) |
| Deploy quickly | Use [V5b CloudFormation](./v5b-cloudformation-regional/) |
| See a specific version | Click the folder above |

## Architecture Evolution

### 🔹 [V1 - Basic Pipeline](./v1-basic-pipeline/)

Simple event-driven processing:

User → S3 → Lambda → DynamoDB + SNS

### 🔹 [V2 - Enhanced Pipeline](./v2-enhanced-pipeline/) (Decoupled + Fault Tolerant)

Introduces message queuing and failure handling:

User → S3 → SQS → Lambda → DynamoDB + SNS
↓
DLQ → CloudWatch Alarm → SNS (Owner Alert)

### 🔹 [V3 - API Gateway & Upload Portal](./v3-api-gateway-portal/)

Adds secure frontend upload via presigned URLs:

User → GitHub Pages → API Gateway → Lambda (GeneratePresignedUrl)
↓
S3 Presigned URL
↓
User → S3 Upload → SQS → Lambda → DynamoDB + SNS

### 🔹 [V4 - Step Functions](./v4-step-functions/) (Workflow Orchestration)

Introduces structured workflow orchestration:

User → GitHub Pages → API Gateway → Lambda (GeneratePresignedUrl)
↓
User → S3 Upload → SQS → Lambda (Trigger)
↓
Step Functions
↓
Validate → Process → Store → Move → Notify
↓
SNS

### 🔹 V5 — CloudFormation (Infrastructure as Code)

- **[V5a](./v5a-cloudformation-basic/)** — Single-region deployment  
- **[V5b](./v5b-cloudformation-regional/)** — Region-aware deployment (avoids naming conflicts)

Same architecture as V4, but fully automated using CloudFormation templates.

## Prerequisites

- AWS Account
- GitHub Account
- Basic understanding of AWS Console navigation

## How to Use This Repository

Each version folder contains:
- **README.md** — Step by step setup instructions
- **lambda/** — Lambda function code
- **policies/** — IAM policy JSON files
- **frontend/** — HTML upload portal (V3 onwards)
- **cloudformation/** — CloudFormation template (V5a and V5b)

Start with V1 and work your way through each version.
Each version builds on the previous one.

## Author

Eyong
