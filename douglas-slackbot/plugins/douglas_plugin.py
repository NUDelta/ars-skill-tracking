from slackbot.bot import respond_to

@respond_to('Give me (.*)')
def giveme(message, something):
    message.reply('Here is {}'.format(something))
