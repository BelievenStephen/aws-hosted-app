# Project 1 Validation Results

## Validation summary

This document records the first successful validation pass for Project 1 after deploying the application behind an Application Load Balancer with ECS Fargate.

## Environment

- **Region:** `us-west-1`
- **ALB DNS:** `aws-hosted-app-alb-152549554.us-west-1.elb.amazonaws.com`
- **Service name:** `aws-hosted-app-service`
- **Cluster name:** `aws-hosted-app-cluster`
- **Task definition:** `aws-hosted-app:2`
- **Target group:** `aws-hosted-app-tg`

## Endpoint results

- **/health**
  - Request: `http://aws-hosted-app-alb-152549554.us-west-1.elb.amazonaws.com/health`
  - Result: `200 OK`
  - Response body: `ok`

- **/**
  - Request: `http://aws-hosted-app-alb-152549554.us-west-1.elb.amazonaws.com/`
  - Result: `200 OK`
  - Response body: `hello`

## Target health result

- **Target health state:** `healthy`
- **Target IP and port:** `172.31.17.21:8080`

## Key ECS service event proof

- ECS reported that the service **started a task**
- ECS reported that the target was **registered** in the target group
- ECS reported that the service **reached a steady state**

## Key CloudWatch log proof

CloudWatch Logs in `/ecs/aws-hosted-app` showed repeated successful health check requests such as:

- `GET /health HTTP/1.1" 200`
- `GET / HTTP/1.1" 200`

This confirmed that:
- the container stayed up
- the app was listening on port `8080`
- the ALB health check path `/health` was working
- the root endpoint `/` was working

## What I checked first

1. Target health in `aws-hosted-app-tg`
2. ECS service desired, running, and pending counts
3. ECS service events
4. CloudWatch Logs in `/ecs/aws-hosted-app`
5. ALB endpoint tests for `/health` and `/`

## Why I trust this result

I trust this validation result because multiple signals agreed with each other:
- target health was `healthy`
- ECS service was `ACTIVE` with desired `1`, running `1`, pending `0`
- ECS reported the service reached a steady state
- CloudWatch Logs showed repeated `200` responses for `/health`
- direct ALB requests returned `200 OK` for both `/health` and `/`

## What proved the system was healthy

The strongest proof was that the ECS service stayed in steady state, the target group reported a healthy target, CloudWatch Logs showed successful health check traffic, and the ALB returned `200 OK` for both `/health` and `/`.
