#!/bin/bash

## Example with only mandatory arguments
python3 06_list_issues.py \
  --newRelicApiKey $NEWRELIC_API_KEY \
  --accountId $NEWRELIC_ACCOUNT_ID \
  --startDateUtc "YOUR_START_TIME_IN_DATETIME_UTC_ISO8601_(%Y-%m-%dT%H:%M:%SZ)"

## Example with custom end date
# python3 06_list_issues.py \
#   --newRelicApiKey $NEWRELIC_API_KEY \
#   --accountId $NEWRELIC_ACCOUNT_ID \
#   --startDateUtc "YOUR_START_TIME_IN_DATETIME_UTC_ISO8601_(%Y-%m-%dT%H:%M:%SZ)" \
#   --endDateUtc "YOUR_START_TIME_IN_DATETIME_UTC_ISO8601_(%Y-%m-%dT%H:%M:%SZ)" \

## Example with alert filtering
# python3 06_list_issues.py \
#   --newRelicApiKey $NEWRELIC_API_KEY \
#   --accountId $NEWRELIC_ACCOUNT_ID \
#   --startDateUtc "YOUR_START_TIME_IN_DATETIME_UTC_ISO8601_(%Y-%m-%dT%H:%M:%SZ)" \
#   --alertPolicyNames "YOUR_ALERT_POLICY_NAMES_AS_CSV_(optional)" \
#   --alertConditionNames "YOUR_ALERT_CONDITION_NAMES_AS_CSV_(optional)"