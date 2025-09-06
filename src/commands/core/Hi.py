from libs import BaseCommand, MessageClass
from libs.MessageClass import clean_number  # import the utility

class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "hi",
                "category": "core",
                "description": {"content": "Say hello to the bot"},
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, _):
        sender_number = clean_number(M.sender.number)
        user = self.client.db.get_user_by_number(sender_number)
        exp = getattr(user, "exp", 0)

        self.client.reply_message(
            f"🎯 Hey *@{sender_number}*! Your current EXP is: *{exp}*.", M
        )
