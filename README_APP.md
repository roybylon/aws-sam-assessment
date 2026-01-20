
# Assignment 1 – Serverless Deployment with AWS SAM

## Architecture
- API Gateway for CRUD endpoints
- AWS Lambda (Python 3.11)
- DynamoDB (PAY_PER_REQUEST)
- IAM Least Privilege via SAM policy templates

## Deployment
```bash
sam build
sam deploy --guided
```

## Endpoints
- POST /items
- GET /items/{id}
- PUT /items/{id}
- DELETE /items/{id}

## Environment Variables
- TABLE_NAME: DynamoDB table name
