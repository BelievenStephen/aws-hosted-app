# Project 1 Architecture Plan (Hosted App Behind ALB)

## Target architecture
Internet → ALB (HTTP/HTTPS listeners) → Target Group → ECS Fargate Service → Tasks (container)

## Traffic + ports
- ALB listeners:
  - HTTP: 80 (initial)
  - HTTPS: 443 (later, after ACM cert)
- Target group:
  - Protocol: HTTP
  - Port: 8080 (container listens here)

## Health checks
- Path: /health
- Expected: HTTP 200
- Reason: target group uses this to determine HealthyHostCount

## Security groups (2-SG model)
### 1) ALB Security Group
Inbound:
- TCP 80 from 0.0.0.0/0 (lab)
- TCP 443 from 0.0.0.0/0 (later)
Outbound:
- TCP 8080 to Target SG (preferred), or 0.0.0.0/0 if you keep it simple initially

### 2) Target (ECS tasks) Security Group
Inbound:
- TCP 8080 from ALB SG only
Outbound:
- All traffic to 0.0.0.0/0 (allows pulling images, reaching AWS APIs if needed)

## Logging + metrics
- App logs: CloudWatch Logs (ECS task log driver)
- ALB metrics (CloudWatch, AWS/ApplicationELB):
  - RequestCount
  - TargetResponseTime
  - HTTPCode_ELB_5XX
  - HTTPCode_Target_5XX
  - HealthyHostCount

## Cost guardrails
- No NAT Gateway for this project (avoid surprise cost)
- 1 ECS service, 1 target group, 1 ALB
- Smallest practical Fargate task size during build
- Teardown documented and executed after tests