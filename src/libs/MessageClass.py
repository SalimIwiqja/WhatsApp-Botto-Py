import re
from libs import Void
from utils import DynamicConfig
from neonize.events import MessageEv


def clean_number(number):
    """Normalize number to digits only with optional '+' at start."""
    if isinstance(number, int):
        number = str(number)
    number = re.sub(r"[^\d+]", "", number)
    if number.startswith("00"):
        number = "+" + number[2:]
    elif number.startswith("0"):
        number = number[1:]
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

        # Sender
        sender_jid_obj = self.Info.MessageSource.Sender
        self.sender_number = clean_number(sender_jid_obj.User)
        self.sender = DynamicConfig(
            {
                "number": self.sender_number,
                "username": getattr(sender_jid_obj, "PushName", "Unknown"),
            }
        )

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
                    quoted_number = clean_number(ctx_info.participant.split("@")[0])
                    contact_obj = client.contact.get_contact(ctx_info.participant)
                    username = (
                        getattr(contact_obj, "PushName", "Unknown")
                        if not isinstance(contact_obj, str)
                        else "Unknown"
                    )
                    self.quoted_user = DynamicConfig(
                        {
                            "number": quoted_number,
                            "username": username,
                        }
                    )

            # Handle mentioned users
            for jid in ctx_info.mentionedJID:
                number = clean_number(jid.split("@")[0])
                contact_obj = client.contact.get_contact(jid)
                username = (
                    getattr(contact_obj, "PushName", "Unknown")
                    if not isinstance(contact_obj, str)
                    else "Unknown"
                )
                self.mentioned.append(
                    DynamicConfig(
                        {
                            "number": number,
                            "username": username,
                        }
                    )
                )

    def build(self):
        # Extract URLs
        self.urls = self.__client.utils.get_urls(self.content)
        # Extract numbers from text and clean them
        self.numbers = [
            clean_number(n) for n in self.__client.utils.extract_numbers(self.content)
        ]

        # Group info
        if self.chat == "group":
            self.group = self.__client.get_group_info(self.gcjid)
            self.isAdminMessage = (
                self.sender.number
                in self.__client.filter_admin_users(self.group.Participants)
            )

        return self

    def raw(self):
        return self.__M
