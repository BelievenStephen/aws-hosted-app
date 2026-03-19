# 5xx Spike Runbook

## Symptoms

- Users report server errors or intermittent failures
- CloudWatch shows a rise in `HTTPCode_ELB_5XX_Count` or `HTTPCode_Target_5XX_Count`
- The site loads inconsistently or fails under normal traffic
- Requests succeed sometimes and fail at other times

## Likely Causes

| Source | Examples |
|---|---|
| ALB-generated 5xx | Listener/routing misconfiguration, ALB-to-target connection issue, bad response from target |
| App-generated 5xx | Application error, unhandled exception, dependency failure |
| Unhealthy targets | Flapping tasks, failed health checks, bad deploy, resource pressure |

## ELB 5xx vs Target 5xx

Identifying the source narrows the investigation significantly:

- **`HTTPCode_ELB_5XX_Count` rises, Target 5xx stays flat** → issue is on the ALB side; investigate listener, routing rules, or the ALB-to-target connection
- **`HTTPCode_Target_5XX_Count` rises** → issue is on the app or target side; investigate application errors, recent deploys, or resource pressure
- **`HealthyHostCount` drops at the same time as either** → start with target health before anything else

## Triage Steps

### 1. Identify the 5xx source

Check in CloudWatch → `AWS/ApplicationELB`:

- `HTTPCode_ELB_5XX_Count`
- `HTTPCode_Target_5XX_Count`
- `HealthyHostCount`
- `RequestCount`
- `TargetResponseTime`

Determine whether errors are ALB-generated, target-generated, or both.

### 2. Check target group health

- Open the target group and review healthy vs. unhealthy target counts
- Confirm health check path is `/health`
- Confirm the app is listening on port `8080`
- Confirm the health check is returning `200`
- Confirm targets are still registered correctly

### 3. Check ECS service events

- Open the ECS service and review the **Events** tab
- Look for failed task launches, deployment issues, or repeated restarts
- Check that desired count matches running count

### 4. Check application logs

- Open CloudWatch Logs for the container log group
- Look for stack traces, unhandled exceptions, or repeated error patterns
- Note the timestamp of the first errors and correlate with any recent deploys or changes

### 5. Check for recent changes

- Was a new image or task definition deployed recently?
- Were any environment variables, secrets, or configs changed?
- Were any upstream dependencies (databases, external APIs) affected?

### 6. Re-test endpoints

- `curl` the ALB DNS name — confirm `/` returns the expected response
- `curl` the `/health` endpoint — confirm it returns `200`
- Note whether errors are consistent or intermittent

## Verification

Confirm all of the following before closing the incident:

- [ ] `HTTPCode_ELB_5XX_Count` and `HTTPCode_Target_5XX_Count` return to baseline
- [ ] `HealthyHostCount` is stable and greater than `0`
- [ ] `/` returns the expected application response
- [ ] `/health` returns `200`
- [ ] No new errors appear in CloudWatch Logs during basic testing
- [ ] ECS service events show no failures or restarts

## Related Runbooks

- [Site down](site-down.md)
- [Security group blocking traffic](security-group-blocking-traffic.md)
- [DNS issues](dns-issues.md)