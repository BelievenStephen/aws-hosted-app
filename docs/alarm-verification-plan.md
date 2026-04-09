# Project 1 — Alarm Verification Plan

## Purpose

This document describes how to verify Project 1 CloudWatch alarms in a low-risk way, without forcing a disruptive live failure. The goal is to confirm each alarm is correctly configured and would respond as expected, while keeping the live deployment stable.

---

## Healthy Baseline

Before running any verification, confirm the deployment is in a known-good state:

| Signal | Expected Value |
|---|---|
| ECS desired / running / pending | `1 / 1 / 0` |
| Target group health | Healthy |
| `/health` response | `200` |
| `/` response | `200` |
| CloudWatch Logs | Repeated `/health 200` entries, no errors |

---

## Alarm: ALB 5xx

**Metric:** `HTTPCode_ELB_5XX_Count`  
**Threshold:** Alarm when count `>= 1`  
**Attached to:** `aws-hosted-app-alb`

### Configuration Verification

Rather than forcing a live failure, verify the alarm is correctly configured:

- Confirm the metric is `HTTPCode_ELB_5XX_Count` under `AWS/ApplicationELB`
- Confirm the threshold is set to alarm when count `>= 1`
- Confirm the alarm is attached to the correct ALB

### Low-Risk Functional Test (Future)

When a safe test environment is available:

1. Deploy a short-lived test service or isolated revision
2. Send a request pattern that produces ALB-level failure behavior in that environment
3. Confirm the alarm transitions to `ALARM` state without affecting the main deployment

### Expected Triage Sequence

If this alarm fires in a live scenario:

1. CloudWatch alarm state changes for this alarm
2. Check ALB metric `HTTPCode_ELB_5XX_Count` for volume and pattern
3. Check ECS service events for task failures or deployment issues
4. Check target group health
5. Review CloudWatch Logs for errors or crashes

### Recovery Confirmation

Before marking the incident resolved:

- [ ] ALB stops recording ELB-generated 5xx responses
- [ ] Alarm returns to `OK`
- [ ] `/health` and `/` return `200`
- [ ] ECS service counts are stable at `1 / 1 / 0`
- [ ] Target group health is `healthy`

---

## Alarm: Healthy Host Count

**Metric:** `HealthyHostCount`  
**Threshold:** Alarm when value `< 1`  
**Attached to:** `aws-hosted-app-tg`

### Configuration Verification

Rather than taking down the live app, verify the alarm is correctly configured:

- Confirm the metric is `HealthyHostCount` under `AWS/ApplicationELB`
- Confirm the threshold is set to alarm when value drops below `1`
- Confirm the alarm is attached to the correct target group

### Low-Risk Functional Test (Future)

When a safe test environment is available:

1. Deploy a temporary test service or isolated revision
2. Force the health check to fail in that test case (e.g., stop the app or return a non-`200` from `/health`)
3. Confirm the target transitions to unhealthy and the alarm moves to `ALARM` state

### Expected Triage Sequence

If this alarm fires in a live scenario:

1. Target group health changes away from `healthy`
2. Alarm transitions toward `ALARM`
3. Check ECS service desired / running / pending counts
4. Review ECS service events for failures or stopped tasks
5. Review CloudWatch Logs for startup errors or crashes
6. Validate `/health` behavior directly if the service is still reachable

### Recovery Confirmation

Before marking the incident resolved:

- [ ] Target group health returns to `healthy`
- [ ] `HealthyHostCount` returns to `1` or higher
- [ ] Alarm returns to `OK`
- [ ] ECS service counts are stable at `1 / 1 / 0`
- [ ] `/health` returns `200`

---

## Notes

This verification plan is intentionally conservative. For a portfolio deployment, the priority is demonstrating that alarms are thoughtfully designed and that a safe verification path exists — not inducing unnecessary downtime in a live environment. Functional alarm testing should be deferred to an isolated test environment.
