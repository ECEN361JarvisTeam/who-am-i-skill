from mycroft import MycroftSkill, intent_file_handler


class WhoAmI(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('i.am.who.intent')
    def handle_i_am_who(self, message):
        recognized = False;
        # Check for matching image

        if recognized:
            self.speak_dialog('i.am.who')
        else:
            self.speak_dialog('i.am.who.unknown')
            # Code to add new face.
            name = self.get_response('i.am.intent')
            self.speak_dialog('i.am.who.known', {'name': name})


def create_skill():
    return WhoAmI()

