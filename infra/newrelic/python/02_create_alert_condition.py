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
  parser.add_argument('--alertPolicyId', help='Alert condition ID.')
  parser.add_argument('--alertConditionName', help='Name of the alert condition.')

  args = parser.parse_args()

  newRelicApiKey = args.newRelicApiKey
  if newRelicApiKey == None:
    print('New Relic API Key is not given!')
    return

  accountId = args.accountId
  if accountId == None:
    print('Account ID is not given!')
    return

  alertPolicyId = args.alertPolicyId
  if alertPolicyId == None:
    print('Alert policy ID is not given!')
    return

  alertConditionName = args.alertConditionName
  if alertConditionName == None:
    print('Alert condition name is not given!')
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
    alertsNrqlConditionStaticCreate(
      policyId: "$alertPolicyId",
      condition: {
        enabled: true,
        name: "$alertConditionName",
        nrql: {
          query: "FROM Transaction SELECT count(*) WHERE appName = 'alert-app' AND (http.statusCode = 400 OR http.statusCode = 500)"
        },
        terms: {
          operator: ABOVE,
          priority: CRITICAL,
          threshold: 0,
          thresholdDuration: 60,
          thresholdOccurrences: AT_LEAST_ONCE
        }
      },
      accountId: $accountId
    ) {
      id
    }
  }
  """)

  # Put variables
  query = queryTemplate.substitute(
    accountId=accountId,
    alertPolicyId=alertPolicyId,
    alertConditionName=alertConditionName,
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
