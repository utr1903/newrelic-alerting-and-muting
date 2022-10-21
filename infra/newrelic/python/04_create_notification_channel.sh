#!/bin/bash

python3 04_create_notification_channel.py \
  --newRelicApiKey $NEWRELIC_API_KEY \
  --accountId $NEWRELIC_ACCOUNT_ID \
  --notificationChannelName "YOUR_NOTIFICATION_CHANNEL_NAME" \
  --notificationDestinationId "YOUR_NOTIFICATION_DESTINATION_ID" \
  --notificationChannelType "YOUR_NOTIFICATION_CHANNEL_TYPE" \
  --notificationChannelKey "YOUR_NOTIFICATION_CHANNEL_KEY" \
  --notificationChannelValue "YOUR_NOTIFICATION_CHANNEL_VALUE"
