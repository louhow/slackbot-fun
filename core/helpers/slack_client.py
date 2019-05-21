from common import bot_slack_client


def get_display_name_for_message(message):
  return bot_slack_client.users[get_user_id(message)]['name']


def get_display_name_for_user_id(id):
  return bot_slack_client.users[id]['name']


def get_user_id(message):
   return message._body['user']
