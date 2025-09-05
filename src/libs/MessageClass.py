import re
from libs import Void
from utils import DynamicConfig
from neonize.events import MessageEv

def clean_number(number):
    """Ensure number is a string and remove any non-digit/non-plus characters."""
    return re.sub(r"[^\d+]", "", str(number))

class MessageClass:
    def __init__(self, client: Void, message: MessageEv):
        self.__client = client
        self.__M = message

        self.Info = message.Info
        self.Message = message.Message
        self.content = client.extract_text(self.Message)
        self.gcjid = self.Info.MessageSource.Chat
        self.chat = "group" if self.Info.MessageSource.IsGroup else "dm"

        sender_number = clean_number(self.Info.MessageSource.Sender.User)
        try:
            contact = client.contact.get_contact(sender_number)
            username = getattr(contact, "PushName", str(sender_number))
        except Exception:
            username = str(sender_number)

        self.sender = DynamicConfig({
            "number": sender_number,
            "username": username,
        })

        self.urls = []
        self.numbers = []
        self.quoted = None
        self.quoted_user = None
        self.mentioned = []

        # Quoted message handling
        if self.Message.HasField("extendedTextMessage"):
            ctx_info = self.Message.extendedTextMessage.contextInfo

            if ctx_info.HasField("quotedMessage"):
                self.quoted = ctx_info.quotedMessage

                if ctx_info.HasField("participant"):
                    quoted_number = clean_number(ctx_info.participant)
                    try:
                        quoted_contact = client.contact.get_contact(quoted_number)
                        quoted_username = getattr(quoted_contact, "PushName", quoted_number)
                    except Exception:
                        quoted_username = quoted_number

                    self.quoted_user = DynamicConfig({
                        "number": quoted_number,
                        "username": quoted_username,
                    })

            # Mentioned users
            for jid in ctx_info.mentionedJID:
                number = clean_number(jid)
                try:
                    contact = client.contact.get_contact(number)
                    username = getattr(contact, "PushName", number)
                except Exception:
                    username = number

                self.mentioned.append(DynamicConfig({
                    "number": number,
                    "username": username,
                }))

    def build(self):
        # Extract URLs and numbers
        self.urls = self.__client.utils.get_urls(self.content)
        self.numbers = [clean_number(n) for n in self.__client.utils.extract_numbers(self.content)]

        # Group info
        if self.chat == "group":
            try:
                self.group = self.__client.get_group_info(self.gcjid)
                self.isAdminMessage = self.sender.number in self.__client.filter_admin_users(self.group.Participants)
            except Exception:
                self.group = None
                self.isAdminMessage = False

        return self

    def raw(self):
        return self.__M
