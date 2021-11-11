from mycroft import MycroftSkill, intent_file_handler


class WhoAmI(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('i.am.who.intent')
    def handle_i_am_who(self, message):
        self.speak_dialog('i.am.who')


def create_skill():
    return WhoAmI()

