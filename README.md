# AWS App Deployment

## What this is
Portfolio project demonstrating how to deploy a simple application in AWS and operate it like a Cloud Support Engineer.  
Includes deployment steps, validation checks, monitoring, incident runbooks, and teardown steps.

## Architecture
High-level target architecture. Final design may evolve.

- Application deployed as a container
- Compute: ECS Fargate (or EC2 initially if needed)
- Traffic: Application Load Balancer (ALB). May be added after a minimal first version
- Logging and metrics: CloudWatch Logs and CloudWatch metrics and alarms

A diagram will be added in `/diagrams`.

## Requirements
- AWS account with an IAM user. MFA enabled
- Basic AWS knowledge. IAM, VPC, EC2 or ECS, CloudWatch
- Local tools when needed:
  - Git
  - Docker
  - AWS CLI. Optional

## Deploy steps
Steps will be documented once the build starts. This section will include:
- Environment setup. VPC and security
- Build and push container image. If applicable
- Deploy service
- Configure logs and alarms
- Confirm access

## Validate steps
This section will include:
- Health check endpoint test
- Expected HTTP responses
- Log verification in CloudWatch
- Alarm verification using a test scenario

## Monitoring and alerts
Planned monitoring includes:
- CloudWatch dashboard for key metrics
- Alarms for common failure modes:
  - Service errors
  - Unhealthy targets
  - Resource pressure
- Log retention settings to control cost

## Security notes
Planned security items include:
- No long-lived access keys for deployment
- IAM roles for compute where possible
- Least privilege for any application permissions
- CloudTrail enabled during build

## Runbooks
Runbooks will be stored in `/runbooks` and will cover:
- Site down or not responding
- 5xx error spike
- DNS or routing issues
- Permission denied. IAM
- Security group blocking traffic

## Teardown
This repo will include step-by-step teardown instructions to avoid unexpected AWS charges.

## Lessons learned
What worked, what broke, what changed, and how the design would be improved.
