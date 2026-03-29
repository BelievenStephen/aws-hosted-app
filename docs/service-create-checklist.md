# ECS Service Creation Checklist

## Purpose

Lock planned values and verify prerequisites before creating the ECS service for Project 1. Keeping ALB creation and ECS service creation in separate sessions reduces the chance of mixing setup mistakes across the two steps.

---

## Planned Service Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| Cluster | `aws-hosted-app-cluster` | Already created |
| Service name | `aws-hosted-app-service` | |
| Task definition | `aws-hosted-app:1` | Current registered revision |
| Launch type | Fargate | |
| Desired count | `1` | Keeps cost low while proving the deploy path |
| Target group | `aws-hosted-app-tg` | Already created |
| Health check path | `/health` | Matches app endpoint and target group config |

---

## Networking Plan

| Resource | Value | Notes |
|----------|-------|-------|
| Network mode | `awsvpc` | Required for Fargate — subnet and SG set at task level |
| Subnets | Selected subnets in `us-west-1` | Record IDs before service creation |
| Task security group | `aws-hosted-app-task-sg` | Accepts inbound on port `8080` from ALB SG only |
| ALB security group | `aws-hosted-app-alb-sg` | Accepts inbound HTTP on port `80` |

---

## Prerequisites Checklist

- [ ] ECS cluster exists: `aws-hosted-app-cluster`
- [ ] Task definition exists: `aws-hosted-app:1`
- [ ] Target group exists: `aws-hosted-app-tg`
- [ ] Task security group exists: `aws-hosted-app-task-sg`
- [ ] ALB security group exists: `aws-hosted-app-alb-sg`
- [ ] ALB exists with an HTTP listener on port `80`
- [ ] Subnet IDs selected and recorded
- [ ] Health check path confirmed: `/health`

---

## Session Order

| Session | Work |
|---------|------|
| Current | Create the ALB and security groups |
| Next | Create the ECS service and attach to `aws-hosted-app-tg` |

---

## Next Step

Once the ALB exists and all prerequisites above are checked off:

1. Create the ECS service inside `aws-hosted-app-cluster`
2. Attach to `aws-hosted-app-tg`
3. Select subnets and `aws-hosted-app-task-sg`
4. Verify target registration and health
5. Validate `GET /health` and `GET /` through the ALB
