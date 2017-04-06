class HelpText(object):
    def __init__(self):
        self.HELP_TEXT = ""

    def add_help_text(self, command_name, command_help):
        help_text = "*" + command_name + "*: "
        help_text += command_help + "\n"
        self.HELP_TEXT += help_text