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
  parser.add_argument('--notificationDestinationName', help='Name of the notification destination.')
  parser.add_argument('--notificationDestinationType', help='Type of the notification destination: EMAIL, JIRA, SLACK...')
  parser.add_argument('--notificationDestinationKey', help='Key of the notification destination (e.g. email).')
  parser.add_argument('--notificationDestinationValue', help='Value of the notification destination (e.g. asdasd@email.com).')

  args = parser.parse_args()

  newRelicApiKey = args.newRelicApiKey
  if newRelicApiKey == None:
    print('New Relic API Key is not given!')
    return

  accountId = args.accountId
  if accountId == None:
    print('Account ID is not given!')
    return

  notificationDestinationName = args.notificationDestinationName
  if notificationDestinationName == None:
    print('Notification destination name is not given!')
    return

  notificationDestinationType = args.notificationDestinationType
  if notificationDestinationType == None:
    print('Notification destination type is not given!')
    return

  notificationDestinationKey = args.notificationDestinationKey
  if notificationDestinationKey == None:
    print('Notification destination key is not given!')
    return

  notificationDestinationValue = args.notificationDestinationValue
  if notificationDestinationValue == None:
    print('Notification destination value is not given!')
    return

  notificationDestinationValue = args.notificationDestinationValue
  if notificationDestinationValue == None:
    print('Notification destination value is not given!')
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
    aiNotificationsCreateDestination(
      destination: {
        name: "$notificationDestinationName",
        properties: {
          displayValue: "$notificationDestinationValue",
          value: "$notificationDestinationValue",
          key: "$notificationDestinationKey"
        },
        type: $notificationDestinationType
      },
      accountId: $accountId
    ) {
      destination {
        id
      }
    }
  }
  """)

  # Put variables
  query = queryTemplate.substitute(
    accountId=accountId,
    notificationDestinationName=notificationDestinationName,
    notificationDestinationValue=notificationDestinationValue,
    notificationDestinationKey=notificationDestinationKey,
    notificationDestinationType=notificationDestinationType,
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
