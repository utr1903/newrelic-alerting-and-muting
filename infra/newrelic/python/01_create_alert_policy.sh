#!/bin/bash

python3 01_create_alert_policy.py \
  --newRelicApiKey $NEWRELIC_API_KEY \
  --accountId $NEWRELIC_ACCOUNT_ID \
  --incidentPreference "YOUR_INCIDENT_PREFERENCE" \
  --alertPolicyName "YOUR_ALERT_POLICY_NAME"
