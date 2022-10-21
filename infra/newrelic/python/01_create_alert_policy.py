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
  parser.add_argument('--incidentPreference', help='Incident preference: PER_CONDITION_AND_TARGET, PER_CONDITION or PER_POLICY.')
  parser.add_argument('--alertPolicyName', help='Name of the alert condition.')

  args = parser.parse_args()

  newRelicApiKey = args.newRelicApiKey
  if newRelicApiKey == None:
    print('New Relic API Key is not given!')
    return

  accountId = args.accountId
  if accountId == None:
    print('Account ID is not given!')
    return

  incidentPreference = args.incidentPreference
  if incidentPreference == None:
    print('Incident preference is not given!')
    return

  alertPolicyName = args.alertPolicyName
  if alertPolicyName == None:
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
    alertsPolicyCreate(
      accountId: $accountId,
      policy: {
        incidentPreference: $incidentPreference,
        name: "$alertPolicyName"
      }
    ) {
      id
    }
  }
  """)

  # Put variables
  query = queryTemplate.substitute(
    accountId=accountId,
    incidentPreference=incidentPreference,
    alertPolicyName=alertPolicyName,
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
