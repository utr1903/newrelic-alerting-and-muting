import argparse
import requests
from string import Template
import time
import datetime

def filterIssue(issue, filteredIssues, filterName, filterConditions):
    for filter in issue[filterName]:
      if str(filter) in filterConditions:
        filteredIssues.append(issue)
        break

def formatDateTime(timestampAsString):
  datetime = convertTimestampToDatetimeUtc(timestampAsString)
  if datetime == None:
    return None
  return "{} ({})".format(datetime.strftime("%Y-%m-%dT%H:%M:%SZ"), timestampAsString)

def convertTimestampToDatetimeUtc(timestampAsString):
  if timestampAsString == None:
    return None
  timestamp = int(timestampAsString)
  timestamp = round(timestamp/1000)
  return datetime.datetime.utcfromtimestamp(timestamp)

def printIssue(issue):
  outputTemplate = Template("""
  ------------------------------------------------
  issueId: $issueId
  policyIds: $policyIds
  policyName: $policyName
  conditionName: $conditionName
  entityGuids: $entityGuids
  createdAt: $createdAt
  activatedAt: $activatedAt
  acknowledgedAt: $acknowledgedAt
  acknowledgedBy: $acknowledgedBy
  closedAt: $closedAt
  closedBy: $closedBy
  ------------------------------------------------
  """)

  output = outputTemplate.substitute(
    issueId=issue["issueId"],
    policyIds=issue["policyIds"],
    policyName=issue["policyName"],
    conditionName=issue["conditionName"],
    entityGuids=issue["entityGuids"],
    createdAt=formatDateTime(issue["createdAt"]),
    activatedAt=formatDateTime(issue["activatedAt"]),
    acknowledgedAt=formatDateTime(issue["acknowledgedAt"]),
    acknowledgedBy=issue["acknowledgedBy"],
    closedAt=formatDateTime(issue["closedAt"]),
    closedBy=issue["closedBy"],
  )

  print(output)

def main():

  ####################################
  ### Parse command line arguments ###
  ####################################
  parser = argparse.ArgumentParser()

  parser.add_argument('--newRelicApiKey', help='New Relic API Key.')
  parser.add_argument('--accountId', help='New Relic Account ID.')
  parser.add_argument('--startDateUtc', help='Start time in UTC format <%Y-%m-%dT%H:%M:%SZ> for the issue search.')
  parser.add_argument('--endDateUtc', help='End time in UTC format <%Y-%m-%dT%H:%M:%SZ> for the issue search. [optional]')
  parser.add_argument('--alertPolicyIds', help='IDs of the alert policies in CSV format. [optional]')
  parser.add_argument('--alertPolicyNames', help='Names of the alert policies in CSV format. [optional]')
  parser.add_argument('--alertConditionNames', help='Names of the alert conditions in CSV format. [optional]')

  args = parser.parse_args()

  newRelicApiKey = args.newRelicApiKey
  if newRelicApiKey == None:
    print('New Relic API Key is not given!')
    return

  accountId = args.accountId
  if accountId == None:
    print('Account ID is not given!')
    return

  startDateUtc = args.startDateUtc
  if startDateUtc == None:
    print('Start time for the issue search is not given!')
    return
  else:
    try:
      startTime = round(datetime.datetime.strptime(startDateUtc, "%Y-%m-%dT%H:%M:%SZ").timestamp() * 1000)
    except:
      print('Start time format is invalid. Should have the following format <%Y-%m-%dT%H:%M:%SZ>')
      return

  endDateUtc = args.endDateUtc
  if endDateUtc == None:
    endTime = round(time.time() * 1000)
  else:
    try:
      endTime = round(datetime.datetime.strptime(endDateUtc, "%Y-%m-%dT%H:%M:%SZ").timestamp() * 1000)
    except:
      print('End time format is invalid. Should have the following format <%Y-%m-%dT%H:%M:%SZ>')
      return

  alertPolicyIds = args.alertPolicyIds
  if alertPolicyIds != None:
    alertPolicyIds = alertPolicyIds.split(",")

  alertPolicyNames = args.alertPolicyNames
  if alertPolicyNames != None:
    alertPolicyNames = alertPolicyNames.split(",")

  alertConditionNames = args.alertConditionNames
  if alertConditionNames != None:
    alertConditionNames = alertConditionNames.split(",")
  #########

  #######################
  ### Execute request ###
  #######################
  headers = {
    "Api-Key": newRelicApiKey,
    "Content-Type": 'application/json'
  }

  nextCursor=""
  allIssues = []

  # Run till all issues are retrieved
  while True:

    queryTemplate = Template("""
    {
      actor {
        account(id: $accountId) {
          aiIssues {
            issues(
              timeWindow: {
                startTime: $startTime,
                endTime: $endTime
              },
              cursor: "$nextCursor",
              filter: {

              }
            ) {
              nextCursor,
              issues {
                issueId
                policyIds
                policyName
                conditionName
                entityGuids
                createdAt
                activatedAt
                acknowledgedAt
                acknowledgedBy
                closedAt
                closedBy
              }
            }
          }
        }
      }
    }
    """)

    # Put variables
    query = queryTemplate.substitute(
      accountId=accountId,
      startTime=startTime,
      endTime=endTime,
      nextCursor=nextCursor,
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

    for issue in result["data"]["actor"]["account"]["aiIssues"]["issues"]["issues"]:
      allIssues.append(issue)

    # Continue to parse till all the data is fetched
    nextCursor = result["data"]["actor"]["account"]["aiIssues"]["issues"]["nextCursor"]
    if nextCursor == None:
      print("All issues are fetched.")
      break
    else:
      print("Issues are not fetched entirely. Continuing...")

  # If no filtering is defined, print all
  if alertPolicyIds == None and alertPolicyNames == None and alertConditionNames == None:
    for issue in allIssues:
      printIssue(issue)

    print("Number of found issues: " + str(len(allIssues)) + "\n")

  # Filter issues
  else:

    filteredIssues = []
    for issue in allIssues:
      
      # Filter according to policy IDs
      if alertPolicyIds != None:
        filterIssue(issue, filteredIssues, "policyIds", alertPolicyIds)
        continue

      # Filter according to policy names
      if alertPolicyNames != None:
        filterIssue(issue, filteredIssues, "policyName", alertPolicyNames)
        continue

      # Filter according to condition names
      if alertConditionNames != None:
        filterIssue(issue, filteredIssues, "conditionName", alertConditionNames)
        continue

    # Print filtered issues
    for issue in filteredIssues:
      printIssue(issue)

    print("Number of found issues: " + str(len(filteredIssues)) + "\n")
  #########

main()
