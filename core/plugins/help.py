from slackbot.bot import respond_to
from common import help_text

@respond_to('help')
def help(message):
    message.reply_webapi('Help Menu', attachments= [{
    "fallback": "Sorry buddy, not sure what you mean.",
    "color": "ADD8E6",
    "text": help_text.HELP_TEXT,
    "mrkdwn_in": ["text", "pretext", "fields"],
  }])
