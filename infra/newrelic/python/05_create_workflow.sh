#!/bin/bash

python3 05_create_workflow.py \
  --newRelicApiKey $NEWRELIC_API_KEY \
  --accountId $NEWRELIC_ACCOUNT_ID \
  --notificationChannelId "YOUR_NOTIFICATION_CHANNEL_ID" \
  --workflowName "YOUR_WORKFLOW_NAME" \
  --alertPolicyIds "YOUR_ALERT_POLICY_IDS_AS_CSV"
