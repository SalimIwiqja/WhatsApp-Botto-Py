import re
from libs import Void
from utils import DynamicConfig
from neonize.events import MessageEv

def clean_number(number):
    # Ensure everything is a string
    number_str = str(number)
    # Keep only digits, allow leading +
    if number_str.startswith("+"):
        return "+" + re.sub(r"[^\d]", "", number_str[1:])
    return "+" + re.sub(r"[^\d]", "", number_str)

class MessageClass:
    def __init__(self, client: Void, message: MessageEv):
        self.__client = client
        self.__M = message

        self.Info = message.Info
        self.Message = message.Message
        self.content = client.extract_text(self.Message)
        self.gcjid = self.Info.MessageSource.Chat
        self.chat = "group" if self.Info.MessageSource.IsGroup else "dm"

        # Always read sender number from metadata and clean it
        sender_jid = str(self.Info.MessageSource.Sender.User)
        self.sender = DynamicConfig({
            "number": "+" + sender_jid if not sender_jid.startswith("+") else sender_jid,
            "username": client.contact.get_contact(sender_jid).PushName,
        })

        self.urls = []
        self.numbers = []
        self.quoted = None
        self.quoted_user = None
        self.mentioned = []

        # Handle quoted messages
        if self.Message.HasField("extendedTextMessage"):
            ctx_info = self.Message.extendedTextMessage.contextInfo

            if ctx_info.HasField("quotedMessage"):
                self.quoted = ctx_info.quotedMessage

                if ctx_info.HasField("participant"):
                    quoted_number = str(ctx_info.participant)
                    if not quoted_number.startswith("+"):
                        quoted_number = "+" + quoted_number
                    self.quoted_user = DynamicConfig({
                        "number": quoted_number,
                        "username": client.contact.get_contact(quoted_number).PushName,
                    })

            # Handle mentions
            for jid in ctx_info.mentionedJID:
                mention_number = str(jid)
                if not mention_number.startswith("+"):
                    mention_number = "+" + mention_number
                self.mentioned.append(DynamicConfig({
                    "number": mention_number,
                    "username": client.contact.get_contact(mention_number).PushName,
                }))

    def build(self):
        # Extract URLs
        self.urls = self.__client.utils.get_urls(self.content)
        # Extract numbers and clean them
        self.numbers = [clean_number(n) for n in self.__client.utils.extract_numbers(self.content)]

        # Group info
        if self.chat == "group":
            self.group = self.__client.get_group_info(self.gcjid)
            self.isAdminMessage = self.sender.number in self.__client.filter_admin_users(self.group.Participants)

        return self

    def raw(self):
        return self.__M
