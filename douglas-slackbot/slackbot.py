import os
from slackclient import SlackClient

auth_token = os.environ["SLACK_BOT_TOKEN"]
slack_client = SlackClient(auth_token)

api_call = slack_client.api_call('users.list')
if api_call.get('ok'):
  users = api_call.get('members')
  for user in users:
    print user.get('name')