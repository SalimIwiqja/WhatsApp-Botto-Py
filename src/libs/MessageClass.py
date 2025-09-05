from libs import Void
from utils import DynamicConfig
from neonize.events import MessageEv
import re

def clean_number(number: str) -> str:
    """Removes invisible unicode chars and ensures only digits with + at the start."""
    number = re.sub(r"[^\d+]", "", number)
    if not number.startswith("+"):
        number = "+" + number
    return number

class MessageClass:
    def __init__(self, client: Void, message: MessageEv):
        self.__client = client
        self.__M = message

        self.Info = message.Info
        self.Message = message.Message
        self.content = client.extract_text(self.Message)
        self.gcjid = self.Info.MessageSource.Chat
        self.chat = "group" if self.Info.MessageSource.IsGroup else "dm"

        sender_number = clean_number(str(self.Info.MessageSource.Sender.User))
        contact = client.contact.get_contact(client.build_jid(sender_number))
        username = contact.PushName if hasattr(contact, "PushName") else "Unknown"

        self.sender = DynamicConfig(
            {
                "number": sender_number,
                "username": username,
            }
        )

        self.urls = []
        self.numbers = []
        self.quoted = None
        self.quoted_user = None
        self.mentioned = []

        if self.Message.HasField("extendedTextMessage"):
            ctx_info = self.Message.extendedTextMessage.contextInfo

            # Handle quoted message
            if ctx_info.HasField("quotedMessage"):
                self.quoted = ctx_info.quotedMessage

                if ctx_info.HasField("participant"):
                    quoted_number = clean_number(ctx_info.participant)
                    quoted_contact = client.contact.get_contact(client.build_jid(quoted_number))
                    quoted_name = quoted_contact.PushName if hasattr(quoted_contact, "PushName") else "Unknown"
                    self.quoted_user = DynamicConfig(
                        {
                            "number": quoted_number,
                            "username": quoted_name,
                        }
                    )

            # Handle mentioned users
            for jid in ctx_info.mentionedJID:
                number = clean_number(jid)
                mention_contact = client.contact.get_contact(client.build_jid(number))
                mention_name = mention_contact.PushName if hasattr(mention_contact, "PushName") else "Unknown"
                self.mentioned.append(
                    DynamicConfig(
                        {
                            "number": number,
                            "username": mention_name,
                        }
                    )
                )

    def build(self):
        self.urls = self.__client.utils.get_urls(self.content)
        self.numbers = [clean_number(n) for n in self.__client.utils.extract_numbers(self.content)]

        if self.chat == "group":
            self.group = self.__client.get_group_info(self.gcjid)
            admins = self.__client.filter_admin_users(self.group.Participants)
            self.isAdminMessage = self.sender.number in admins

        return self

    def raw(self):
        return self.__M
