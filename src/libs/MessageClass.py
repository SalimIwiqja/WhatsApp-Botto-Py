import re
from libs import Void
from utils import DynamicConfig

def jid_to_number(jid: str) -> str:
    if "@" in jid:
        number = jid.split("@")[0]
        if not number.startswith("+"):
            number = f"+{number}"
        return number
    return jid

class MessageClass:
    def __init__(self, client: Void, message):
        self.__client = client
        self.__M = message

        self.Info = message.Info
        self.Message = message.Message
        self.content = client.extract_text(self.Message)
        self.gcjid = self.Info.MessageSource.Chat
        self.chat = "group" if self.Info.MessageSource.IsGroup else "dm"

        sender_jid = self.Info.MessageSource.Sender.User
        sender_number = jid_to_number(sender_jid)
        sender_username = "Unknown"

        try:
            contact = client.contact.get_contact(sender_jid)
            if hasattr(contact, "PushName"):
                sender_username = contact.PushName
        except Exception:
            sender_username = "Unknown"

        self.sender = DynamicConfig({"number": sender_number, "username": sender_username})

        self.urls = []
        self.numbers = []
        self.quoted = None
        self.quoted_user = None
        self.mentioned = []

        # handle quoted message
        if self.Message.HasField("extendedTextMessage"):
            ctx_info = self.Message.extendedTextMessage.contextInfo

            if ctx_info.HasField("quotedMessage"):
                self.quoted = ctx_info.quotedMessage

                if ctx_info.HasField("participant"):
                    quoted_number = jid_to_number(ctx_info.participant)
                    quoted_username = "Unknown"
                    try:
                        contact = client.contact.get_contact(ctx_info.participant)
                        if hasattr(contact, "PushName"):
                            quoted_username = contact.PushName
                    except Exception:
                        quoted_username = "Unknown"
                    self.quoted_user = DynamicConfig(
                        {"number": quoted_number, "username": quoted_username}
                    )

            # handle mentioned JIDs
            for jid in ctx_info.mentionedJID:
                number = jid_to_number(jid)
                mention_username = "Unknown"
                try:
                    contact = client.contact.get_contact(jid)
                    if hasattr(contact, "PushName"):
                        mention_username = contact.PushName
                except Exception:
                    mention_username = "Unknown"
                self.mentioned.append(
                    DynamicConfig({"number": number, "username": mention_username})
                )

    def build(self):
        self.urls = self.__client.utils.get_urls(self.content)
        self.numbers = [
            str(n) if isinstance(n, int) else n
            for n in self.__client.utils.extract_numbers(self.content)
        ]
        if self.chat == "group":
            self.group = self.__client.get_group_info(self.gcjid)
            self.isAdminMessage = (
                self.sender.number
                in self.__client.filter_admin_users(self.group.Participants)
            )
        return self

    def raw(self):
        return self.__M
