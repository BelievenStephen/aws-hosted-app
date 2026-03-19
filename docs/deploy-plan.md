# Deploy Plan

## Purpose

This document outlines the planned deployment of a minimal containerized Python app on Amazon ECS Fargate behind an Application Load Balancer. The goal is to demonstrate a support-minded deployment that includes health checks, CloudWatch Logs, validation steps, and teardown steps for cost control.

## Architecture

| Component | Detail |
|---|---|
| Compute | ECS Fargate |
| Ingress | Application Load Balancer (ALB) |
| Container port | `8080` |
| Health check path | `/health` → returns `200` |
| Container registry | Amazon ECR |
| Logging | CloudWatch Logs (`awslogs` driver) |
| Region | `us-west-1` |

**Security groups:**
- ALB SG: inbound `80`/`443` from internet, outbound to Target SG on `8080`
- Target SG: inbound `8080` from ALB SG only, outbound `0.0.0.0/0`

## Prerequisites

Before starting, confirm the following are in place:

- [ ] AWS account with a budget alert enabled
- [ ] IAM identity with MFA enabled and permissions for:
  - Amazon ECR
  - Amazon ECS
  - Elastic Load Balancing
  - IAM PassRole (where required)
  - CloudWatch Logs
- [ ] AWS CLI installed and configured for `us-west-1`
- [ ] Docker installed and working locally
- [ ] App running locally on port `8080`
- [ ] ECR repository created for image storage

## Deployment Steps

### 1. Build the Docker image locally

- Build the image from `app/Dockerfile`
- Confirm the container starts and responds on port `8080`
- Confirm `/health` returns `200` before pushing

### 2. Tag the image for Amazon ECR

- Tag the local image with the ECR repository URI
- Use a consistent naming convention (e.g., `app:latest` or `app:<git-sha>`)

### 3. Push the image to Amazon ECR

- Authenticate Docker to the ECR private registry using the AWS CLI
- Push the tagged image to the ECR repository

### 4. Create the ECS task definition

- Launch type: Fargate
- Container port: `8080`
- Health check path: `/health`
- Log driver: `awslogs` (CloudWatch Logs)
- Keep CPU and memory values minimal for cost control

### 5. Create the ECS cluster and service

- Create or reuse a cluster scoped to this project
- Create a service referencing the task definition
- Set desired count to `1` initially

### 6. Create the target group

- Protocol: HTTP, port `8080`
- Health check path: `/health`
- Dedicate this target group to this service only

### 7. Create the Application Load Balancer and listener

- Create an ALB in public subnets
- Attach the ALB security group
- Create an HTTP listener on port `80`
- Forward listener traffic to the target group

### 8. Attach the ECS service to the target group

- Configure the ECS service to register tasks with the target group
- Wait for targets to pass health checks before validating

## Validation Checklist

Run these checks after deployment to confirm the service is healthy:

- [ ] ALB DNS name responds in the browser or via `curl`
- [ ] `/` returns the expected application response
- [ ] `/health` returns `200` with the expected response body
- [ ] Target group shows all targets as healthy
- [ ] CloudWatch Logs contains container output
- [ ] No ELB 5xx or Target 5xx errors during basic testing

## Teardown Checklist

Run these steps in order to avoid unexpected AWS charges:

- [ ] Delete ECS service (set desired count to `0` first)
- [ ] Stop any remaining ECS tasks
- [ ] Delete the ALB listener
- [ ] Delete the ALB
- [ ] Delete the target group
- [ ] Deregister task definition revisions
- [ ] Delete ECR images
- [ ] Delete the ECR repository
- [ ] Delete project-specific security groups
- [ ] Confirm no remaining billable resources (check AWS Cost Explorer or Billing dashboard)

## Notes

- No NAT Gateway planned — keep networking simple and cost-free where possible
- Run and validate the app locally on port `8080` before deploying to AWS — reduces cloud troubleshooting time significantly
- This plan may evolve; see the [architecture diagram](../diagrams/architecture.md) for the latest design