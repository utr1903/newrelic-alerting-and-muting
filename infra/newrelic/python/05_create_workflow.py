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
  parser.add_argument('--notificationChannelId', help='ID of the notification channel.')
  parser.add_argument('--workflowName', help='Name of the workflow.')
  parser.add_argument('--alertPolicyIds', help='IDs of the alert policies in CSV format.')

  args = parser.parse_args()

  newRelicApiKey = args.newRelicApiKey
  if newRelicApiKey == None:
    print('New Relic API Key is not given!')
    return

  accountId = args.accountId
  if accountId == None:
    print('Account ID is not given!')
    return

  notificationChannelId = args.notificationChannelId
  if notificationChannelId == None:
    print('Notification channel ID is not given!')
    return

  workflowName = args.workflowName
  if workflowName == None:
    print('Workflow name is not given!')
    return

  alertPolicyIds = args.alertPolicyIds
  if alertPolicyIds == None:
    print('Alert policy ID(s) are not given!')
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
    aiWorkflowsCreateWorkflow(createWorkflowData: {
      destinationConfigurations: {
        channelId: "$notificationChannelId"
      },
      mutingRulesHandling: NOTIFY_ALL_ISSUES,
      workflowEnabled: true,
      name: "$workflowName",
      destinationsEnabled: true,
      issuesFilter: {
        name: "Test",
        predicates: {
          attribute: "labels.policyIds",
          operator: CONTAINS,
          values: "$alertPolicyIds"
        },
        type: FILTER
      }
    },
    accountId: $accountId
  ) {
      workflow {
        id
      }
      errors {
        type
        description
      }
    }
  }
  """)

  # Put variables
  query = queryTemplate.substitute(
    accountId=accountId,
    notificationChannelId=notificationChannelId,
    workflowName=workflowName,
    alertPolicyIds=alertPolicyIds,
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
