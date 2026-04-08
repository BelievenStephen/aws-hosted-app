# Project 1 — Teardown and Cost Control

## Purpose

This document covers how to safely tear down Project 1 resources in the correct dependency order to avoid unnecessary charges and reduce cleanup mistakes.

---

## Teardown Order

Delete resources in this order to avoid dependency conflicts:

| Step | Resource |
|---|---|
| 1 | ECS service |
| 2 | Application Load Balancer |
| 3 | Target group |
| 4 | CloudWatch alarms |
| 5 | CloudWatch dashboard |
| 6 | ECR images and repository |
| 7 | Task definition revisions (optional) |

---

## Step-by-Step Instructions

### 1. Delete the ECS Service

1. Open **ECS** → select cluster `aws-hosted-app-cluster`
2. Open service `aws-hosted-app-service`
3. If tasks are still running, update the desired count to `0` and wait for them to stop
4. Delete the service
5. Confirm no running tasks remain in the cluster before continuing

### 2. Delete the ALB

1. Open **EC2** → **Load Balancers**
2. Select `aws-hosted-app-alb` and delete it
3. Confirm the ALB is fully removed before moving to the target group

### 3. Delete the Target Group

1. Open **EC2** → **Target Groups**
2. Select `aws-hosted-app-tg` and delete it

### 4. Delete CloudWatch Alarms

Delete the following alarms:

- `aws-hosted-app-alb-5xx-alarm`
- `aws-hosted-app-healthy-host-count-alarm`

Removing these prevents leftover alarm clutter and avoids confusion in future projects.

### 5. Delete the CloudWatch Dashboard

Delete the following dashboard:

- `aws-hosted-app-dashboard`

### 6. Delete ECR Images and Repository

1. Open **Amazon ECR**
2. Open repository `aws-hosted-app`
3. Delete all images in the repository
4. Delete the repository if it is no longer needed

> **Note:** ECR storage persists independently of ECS and will continue to exist until explicitly deleted. This is one of the more important cleanup steps for cost control.

### 7. Task Definition Cleanup (Optional)

Task definition revisions do not generate meaningful ongoing cost, but old revisions can create clutter in the console.

After the service is deleted, review the `aws-hosted-app` task definition family:

- Keep the latest revision if you want a record of the configuration
- Deregister older revisions for cleaner project hygiene

---

## Final Checklist

Confirm all of the following before considering teardown complete:

- [ ] ECS service deleted
- [ ] No ECS tasks still running
- [ ] ALB deleted
- [ ] Target group deleted
- [ ] CloudWatch alarms deleted
- [ ] CloudWatch dashboard deleted
- [ ] ECR images deleted
- [ ] ECR repository deleted (if no longer needed)
- [ ] Any security groups created exclusively for this project removed
- [ ] Budget alerts still active for future work

---

## Portfolio Note

For documentation and validation purposes, it is reasonable to leave the project deployed temporarily while recording the confirmed healthy state. If keeping the deployment running, review costs regularly and keep the configuration as minimal as possible.
