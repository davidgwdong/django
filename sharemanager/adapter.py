from allauth.account.adapter import DefaultAccountAdapter

class XPAdapter(DefaultAccountAdapter):
    def add_message(self, request, level, message_template,
                        message_context=None, extra_tags=''):
        print("xp adapter add_message ")
        pass
