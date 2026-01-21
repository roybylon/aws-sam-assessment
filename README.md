# AWS SAM Serverless CRUD API Project

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Architecture](#architecture)  
3. [Requirements](#requirements)  
4. [Setup & Deployment](#setup--deployment)  
5. [CI/CD Pipeline](#cicd-pipeline)  
6. [IAM Permissions](#iam-permissions)  
7. [Testing](#testing)  
8. [File Structure](#file-structure)  
9. [Future Improvements](#future-improvements)

---

## Project Overview
This project implements a **serverless CRUD API** using **AWS SAM**. The application allows users to create, read, update, and delete items stored in a **DynamoDB** table via **Lambda functions** exposed through **API Gateway**.

**Key Features:**
- Serverless infrastructure (API Gateway, Lambda, DynamoDB)
- Fully deployable with a single command
- CI/CD pipeline for automated deployment
- PEP8 linting enforced in Python functions

---

## Architecture

```
Client
   │
   ▼
API Gateway
   │
   ▼
Lambda Functions
   ├── Create Item (POST)
   ├── Read Item (GET)
   ├── Update Item (PUT)
   └── Delete Item (DELETE)
   │
   ▼
DynamoDB Table
```

- **AWS SAM** manages the infrastructure as code.
- **GitHub Actions** automates building, testing, and deploying the stack.

---

## Requirements

- **AWS CLI** configured with credentials having sufficient permissions  
- **SAM CLI** installed (`sam --version`)  
- **Python 3.11+** (for Lambda functions)  
- **Git** for cloning repository and version control  

Optional:
- `flake8` for linting Python code
- `black` for auto-formatting

---

## Setup & Deployment

### 1. Clone the Repository
```bash
git clone https://github.com/roybylon/aws-sam-assessment-.git
cd aws-sam-assessment-
```

### 2. Install Dependencies
```bash
cd src
pip install -r requirements.txt
```
> **Note:** `requirements.txt` may be empty if no external dependencies are required.

### 3. Build the SAM Application
```bash
sam build
```

### 4. Deploy the Application
#### Locally (guided)
```bash
sam deploy --guided
```

#### In CI / non-interactive
```bash
sam deploy \
  --stack-name sam-cicd-stack \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset \
  --resolve-s3
```

### 5. Test API
Use `curl` or Postman with the API Gateway URL provided after deployment.

Example:
```bash
curl -X POST https://<api-id>.execute-api.<region>.amazonaws.com/Prod/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Sample Item"}'
```

---

## CI/CD Pipeline

- **GitHub Actions** automates deployment when code is pushed to `main`.
- Steps include:
  1. Linting with **flake8**
  2. Building Lambda function (`sam build`)
  3. Deploying stack (`sam deploy --resolve-s3`)
  4. Optional: Run tests after deployment
- Secrets used:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - (Optional) `AWS_REGION`

### Pipeline YAML snippet:
```yaml
- name: Configure AWS Credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1
```

---

## IAM Permissions

The deployment requires the following IAM permissions:

- CloudFormation: `CreateChangeSet`, `ExecuteChangeSet`, `DescribeStacks`, `DeleteStack`
- IAM: `CreateRole`, `AttachRolePolicy`, `PassRole`
- Lambda: Full access for function creation
- S3: Create buckets and upload artifacts
- API Gateway: Full access
- DynamoDB: Table creation and access

> **Tip:** For assessment or testing purposes, using AWS-managed policies like `AWSCloudFormationFullAccess`, `AWSLambdaFullAccess`, and `AmazonDynamoDBFullAccess` simplifies setup. For production, apply **least privilege**.

---

## Testing

- **Local tests:**
```bash
sam local invoke ApiFunction --event events/event.json
```

- **Cloud tests:**
```bash
sam sync --stack-name sam-cicd-stack --watch
```

- Linting:
```bash
flake8 src/
```

---

## File Structure

```
aws-sam-assessment-/
│
├── src/
│   ├── app.py          # Lambda CRUD functions
│   └── requirements.txt
│
├── template.yaml       # SAM template
├── .github/workflows/
│   └── deploy.yml      # CI/CD pipeline
└── README.md           # Project documentation
```

---

## Future Improvements

- Add **unit tests** and integration tests for Lambda functions
- Separate Lambda functions per CRUD operation
- Add **staging and production stages** with separate stacks
- Implement **envi
