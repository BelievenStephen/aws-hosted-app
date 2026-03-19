# Site Down Runbook

## Symptoms

- The application does not load through the ALB DNS name
- Browser shows `5xx` errors, a connection timeout, or "site can't be reached"
- `curl` to the ALB DNS name fails or returns an unexpected response
- Users report the site is unavailable or intermittently unreachable

## Likely Causes

| Area | Examples |
|---|---|
| ALB | Listener missing or misconfigured, listener rule not forwarding correctly |
| Target group | No healthy targets, wrong health check path or port |
| ECS service | Tasks not running, failed launches, desired count mismatch |
| Security groups | ALB SG or Target SG blocking traffic on port `8080` |
| Application | Not listening on port `8080`, `/health` returning non-`200`, crashing on start |

## Triage Steps

### 1. Check the ALB

- Confirm the ALB exists and is in an **active** state
- Confirm the listener is present and forwarding to the correct target group
- `curl` the ALB DNS name and note the response or error
```bash
curl -i http://<alb-dns-name>
```

- Check CloudWatch → `AWS/ApplicationELB` for:
  - `HealthyHostCount`
  - `HTTPCode_ELB_5XX_Count`
  - `HTTPCode_Target_5XX_Count`

### 2. Check target group health

- Open the target group and review healthy vs. unhealthy target counts
- Confirm the health check path is `/health`
- Confirm the health check port matches the container port (`8080`)
- If targets are unhealthy, note whether it is a connection failure or a non-`200` response

### 3. Check the ECS service

- Open the ECS service and confirm the running count matches the desired count
- Review the **Events** tab for failed task launches, stopped tasks, or deployment errors
- Confirm the task definition references the correct image and container port (`8080`)

### 4. Check application logs

- Open CloudWatch Logs for the container log group
- Look for startup errors, crashes, or repeated failure patterns
- Confirm the app started successfully and is listening on port `8080`

### 5. Check security groups

- **ALB SG**: confirm inbound rules allow `80`/`443` from the internet, and outbound allows traffic to the Target SG on port `8080`
- **Target SG**: confirm inbound allows port `8080` from the ALB SG only
- If rules look correct, confirm the right security groups are actually attached to the ALB and ECS tasks

### 6. Test endpoints directly

Test locally first to confirm the app itself is healthy before re-testing via the ALB:
```bash
# Local health check
curl -i http://localhost:8080/health

# ALB health check
curl -i http://<alb-dns-name>/health
```

Expected: `200` with the expected response body on both.

## Verification

Confirm all of the following before closing the incident:

- [ ] ALB DNS name loads the expected application response
- [ ] `/health` returns `200`
- [ ] Target group shows all targets as healthy
- [ ] `HealthyHostCount` is stable and greater than `0`
- [ ] ECS running count matches desired count
- [ ] No errors or crashes in CloudWatch Logs
- [ ] No active `HTTPCode_ELB_5XX_Count` or `HTTPCode_Target_5XX_Count` alarms

## Related Runbooks

- [5xx spike](5xx-spike.md)
- [Security group blocking traffic](security-group-blocking-traffic.md)
- [DNS issues](dns-issues.md)