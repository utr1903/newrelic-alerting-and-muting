import argparse
import requests
from string import Template

def main():

  ####################################
  ### Parse command line arguments ###
  ####################################
  parser = argparse.ArgumentParser()

  parser.add_argument('--newRelicApiKey', help='New Relic API Key.')
  parser.add_argument('--accountId', help='New Relic Account ID.')
  parser.add_argument('--notificationChannelName', help='Name of the notification channel.')
  parser.add_argument('--notificationDestinationId', help='ID of the notification destination.')
  parser.add_argument('--notificationChannelType', help='Type of the notification channel: EMAIL, JIRA, SLACK...')
  parser.add_argument('--notificationChannelKey', help='Key of the notification channel (e.g. email).')
  parser.add_argument('--notificationChannelValue', help='Value of the notification channel (e.g. asdasd@email.com).')

  args = parser.parse_args()

  newRelicApiKey = args.newRelicApiKey
  if newRelicApiKey == None:
    print('New Relic API Key is not given!')
    return

  accountId = args.accountId
  if accountId == None:
    print('Account ID is not given!')
    return

  notificationChannelName = args.notificationChannelName
  if notificationChannelName == None:
    print('Notification channel name is not given!')
    return

  notificationDestinationId = args.notificationDestinationId
  if notificationDestinationId == None:
    print('Notification destination ID is not given!')
    return

  notificationChannelType = args.notificationChannelType
  if notificationChannelType == None:
    print('Notification channel type is not given!')
    return

  notificationChannelKey = args.notificationChannelKey
  if notificationChannelKey == None:
    print('Notification channel key is not given!')
    return

  notificationChannelValue = args.notificationChannelValue
  if notificationChannelValue == None:
    print('Notification channel value is not given!')
    return
  #########

  #######################
  ### Execute request ###
  #######################
  headers = {
    "Api-Key": newRelicApiKey,
    "Content-Type": 'application/json'
  }

  queryTemplate = Template("""
  mutation {
    aiNotificationsCreateChannel(
      accountId: $accountId,
      channel: {
        destinationId: "$notificationDestinationId",
        name: "$notificationChannelName",
        product: ALERTS,
        properties: {
          displayValue: "$notificationChannelValue",
          value: "$notificationChannelValue",
          key: "$notificationChannelKey"
        },
        type: $notificationChannelType
      }
    ) {
      channel {
        id
      }
      error {
        ... on AiNotificationsResponseError {
          description
          details
          type
        }
        ... on AiNotificationsDataValidationError {
          details
          fields {
            field
            message
          }
        }
        ... on AiNotificationsConstraintsError {
          constraints {
            dependencies
            name
          }
        }
      }
    }
  }
  """)

  # Put variables
  query = queryTemplate.substitute(
    accountId=accountId,
    notificationChannelName=notificationChannelName,
    notificationDestinationId=notificationDestinationId,
    notificationChannelValue=notificationChannelValue,
    notificationChannelKey=notificationChannelKey,
    notificationChannelType=notificationChannelType,
  )

  # Execute request
  request = requests.post(
    'https://api.eu.newrelic.com/graphql',
    json={'query': query},
    headers=headers
  )

  if request.status_code != 200:
    print("Query failed to run by returning code of {}. {}".format(request.status_code, query))
    return

  result = request.json()
  print(result)
  #########

main()
