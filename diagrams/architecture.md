# Architecture Diagram (Placeholder)

Internet
  |
  v
ALB (80/443)
  |
  v
Target Group (HTTP:8080, health: /health)
  |
  v
ECS Fargate Service
  |
  v
Task(s): container on :8080