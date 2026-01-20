
# Assignment 2 – CI/CD Pipeline for Serverless Application

## Tooling
- GitHub Actions
- AWS SAM
- AWS IAM

## Trigger
- Push to `main` branch

## Pipeline Steps
1. Checkout source code
2. Setup Python & SAM CLI
3. Configure AWS credentials
4. Run lint checks
5. Build & deploy Lambda using SAM

## Required Secrets
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

## Rollback
- CloudFormation automatically rolls back on failure
