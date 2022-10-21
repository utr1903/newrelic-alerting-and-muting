#!/bin/bash

python3 03_create_notification_destination.py \
  --newRelicApiKey $NEWRELIC_API_KEY \
  --accountId $NEWRELIC_ACCOUNT_ID \
  --notificationDestinationName "YOUR_NOTIFICATION_DESTINATION_NAME" \
  --notificationDestinationType "YOUR_NOTIFICATION_DESTINATION_TYPE" \
  --notificationDestinationKey "YOUR_NOTIFICATION_DESTINATION_KEY" \
  --notificationDestinationValue "YOUR_NOTIFICATION_DESTINATION_VALUE"
