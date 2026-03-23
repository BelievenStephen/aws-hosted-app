# Deployment Values

## Purpose

This file locks the planned names and settings for Project 1 before creating the ECS task definition, service, target group, and ALB. The goal is to reduce setup mistakes by keeping one clear source of truth for the deployment values.

## Core AWS Settings

- **AWS region:** `us-west-1`
  - Why: This is the lab region already used for most of the project work and keeps the deployment consistent with the rest of the environment.

- **ECR repo name:** `aws-hosted-app`
  - Why: This matches the image repository already created and pushed for Project 1.

## ECS Settings

- **Cluster name:** `aws-hosted-app-cluster`
  - Why: Clear, project-specific name that will be easy to recognize in the ECS console.

- **Service name:** `aws-hosted-app-service`
  - Why: Makes it obvious which ECS service belongs to this project.

- **Task definition family:** `aws-hosted-app`
  - Why: Keeps the task definition family aligned with the repo and container image naming.

- **Container name:** `aws-hosted-app`
  - Why: Simple and consistent with the task family and ECR repo name.

- **ECS launch type:** `Fargate`
  - Why: This project is planned as an ECS Fargate deployment and avoids managing EC2 worker nodes.

- **Desired count:** `1`
  - Why: Keeps cost low while still proving the deployment path and service behavior.

## Container and Health Settings

- **Container port:** `8080`
  - Why: The app is already built and validated locally on port 8080.

- **Health check path:** `/health`
  - Why: The app already returns a healthy response on `/health`, which makes it a good ALB target group health check path.

## Load Balancer Settings

- **ALB scheme:** `internet-facing`
  - Why: The application needs to be reachable from the browser or curl during validation.

- **Listener port:** `80`
  - Why: Simple first listener for HTTP validation before adding any HTTPS complexity.

- **Target group name:** `aws-hosted-app-tg`
  - Why: Clear project-specific name that matches the ECS service it will support.

## Logging Settings

- **Log group name:** `/ecs/aws-hosted-app`
  - Why: Matches common ECS naming style and keeps app container logs easy to find in CloudWatch Logs.

## Security Group Plan

- **ALB security group:** `aws-hosted-app-alb-sg`
  - Why: Keeps ALB traffic rules separate from application task rules.

- **Task security group:** `aws-hosted-app-task-sg`
  - Why: Makes it clear this security group belongs to the ECS tasks, not the load balancer.

### Planned security group behavior

- **ALB SG allows inbound HTTP**
  - Why: The ALB needs to receive client traffic on port 80.

- **Task SG allows app port from ALB SG only**
  - Why: The app should only receive traffic from the ALB, not directly from the internet.

## Summary of Planned Names

- Region: `us-west-1`
- ECR repo: `aws-hosted-app`
- ECS cluster: `aws-hosted-app-cluster`
- ECS service: `aws-hosted-app-service`
- Task definition family: `aws-hosted-app`
- Container name: `aws-hosted-app`
- Container port: `8080`
- Health check path: `/health`
- Launch type: `Fargate`
- Desired count: `1`
- ALB scheme: `internet-facing`
- Listener port: `80`
- Target group: `aws-hosted-app-tg`
- Log group: `/ecs/aws-hosted-app`
- ALB SG: `aws-hosted-app-alb-sg`
- Task SG: `aws-hosted-app-task-sg`

## What this prepares for next

This checklist prepares the next deployment steps:
1. create or confirm the CloudWatch log group
2. create or confirm the task execution role
3. register the ECS task definition
4. create the target group with `/health`
5. create the ECS cluster and service
6. create the ALB and listener
7. validate `/health` and `/`