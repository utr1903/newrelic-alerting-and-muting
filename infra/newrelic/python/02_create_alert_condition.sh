#!/bin/bash

python3 02_create_alert_condition.py \
  --newRelicApiKey $NEWRELIC_API_KEY \
  --accountId $NEWRELIC_ACCOUNT_ID \
  --alertPolicyId "YOUR_ALERT_POLICY_ID" \
  --alertConditionName "YOUR_ALERT_CONDITION_NAME"
