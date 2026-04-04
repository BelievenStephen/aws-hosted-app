# AWS App Deployment

## What this is
Portfolio project demonstrating how to deploy a simple application in AWS and operate it like a Cloud Support Engineer.  
Includes deployment steps, validation checks, monitoring, incident runbooks, and teardown steps.

## Decisions
- Compute: ECS Fargate
- Container port: 8080
- Health check: `GET /health` returns `200`
- Security groups:
  - ALB SG: inbound 80/443 from internet, outbound to target SG on 8080
  - Target SG: inbound 8080 from ALB SG only, outbound 0.0.0.0/0

## Architecture
High-level target architecture. Final design may evolve.
- Application deployed as a container
- Compute: ECS Fargate (or EC2 initially if needed)
- Traffic: Application Load Balancer (ALB). May be added after a minimal first version
- Logging and metrics: CloudWatch Logs and CloudWatch metrics and alarms

A diagram will be added in `/diagrams`.  
See: [Architecture diagram](diagrams/architecture.md)

## Current Deployed State
Project 1 is deployed on **ECS Fargate** behind an **Application Load Balancer** in `us-west-1`.

| Detail | Value |
|--------|-------|
| ECS service | `aws-hosted-app-service` |
| ECS cluster | `aws-hosted-app-cluster` |
| Task definition | `aws-hosted-app:2` |
| Target group | `aws-hosted-app-tg` |
| Health check path | `/health` |
| ALB DNS | `aws-hosted-app-alb-[redacted].us-west-1.elb.amazonaws.com` |

## Deployment and Operations Docs
- [Deploy plan](docs/deploy-plan.md)
- [Site down runbook](runbooks/site-down.md)
- [5xx spike runbook](runbooks/5xx-spike.md)
- [DNS issues runbook](runbooks/dns-issues.md)
- [Security group blocking traffic runbook](runbooks/security-group-blocking-traffic.md)
- [Validation results](docs/validation-results.md)

## Requirements
- AWS account with an IAM user. MFA enabled
- Basic AWS knowledge. IAM, VPC, EC2 or ECS, CloudWatch
- Local tools when needed:
  - Git
  - Docker
  - AWS CLI. Optional

## Deploy Steps
Steps will be documented once the build starts. This section will include:
- Environment setup. VPC and security
- Build and push container image. If applicable
- Deploy service
- Configure logs and alarms
- Confirm access

## Validate Steps
Use the ALB DNS to validate the deployment.

**Health endpoint**
```bash
curl -i http://aws-hosted-app-alb-[redacted].us-west-1.elb.amazonaws.com/health
```
Expected: `200 OK` — body: `ok`

**Root endpoint**
```bash
curl -i http://aws-hosted-app-alb-[redacted].us-west-1.elb.amazonaws.com/
```
Expected: `200 OK` — body: `hello`

Additional validation checklist:
- Health check endpoint test
- Expected HTTP responses
- Log verification in CloudWatch
- Alarm verification using a test scenario

## Monitoring and Alerts
Planned monitoring includes:
- CloudWatch dashboard for key metrics
- Alarms for common failure modes:
  - Service errors
  - Unhealthy targets
  - Resource pressure
- Log retention settings to control cost

## Security Notes
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

## Lessons Learned
- The ECS service can be created successfully even when the container still fails at runtime, so service creation alone is not proof that the app is healthy.
- The first failed deployment was caused by a CPU architecture mismatch. Updating the task definition to use the ARM64 runtime platform fixed the `exec format error`.
- The fastest checks were ECS service events, target health, and CloudWatch Logs.
