import re
from libs import Void
from utils import DynamicConfig
from neonize.events import MessageEv


def clean_number(number):
    """Normalize WhatsApp numbers to plain digits with +"""
    if not number:
        return ""
    number = str(number)
    number = re.sub(r"[^\d+]", "", number)
    if not number.startswith("+"):
        number = "+" + number.lstrip("0")
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

        raw_sender = self.Info.MessageSource.Sender.User
        sender_jid = clean_number(raw_sender)

        try:
            contact = client.contact.get_contact(sender_jid)
            self.sender = DynamicConfig(
                {
                    "number": sender_jid,
                    "username": getattr(contact, "PushName", "Unknown"),
                }
            )
        except Exception:
            self.sender = DynamicConfig({"number": sender_jid, "username": "Unknown"})

        self.urls = []
        self.numbers = []
        self.quoted = None
        self.quoted_user = None
        self.mentioned = []

        if self.Message.HasField("extendedTextMessage"):
            ctx_info = self.Message.extendedTextMessage.contextInfo

            if ctx_info.HasField("quotedMessage"):
                self.quoted = ctx_info.quotedMessage
                if ctx_info.HasField("participant"):
                    quoted_number = clean_number(ctx_info.participant.split("@")[0])
                    try:
                        contact = client.contact.get_contact(quoted_number)
                        self.quoted_user = DynamicConfig(
                            {
                                "number": quoted_number,
                                "username": getattr(contact, "PushName", "Unknown"),
                            }
                        )
                    except Exception:
                        self.quoted_user = DynamicConfig(
                            {"number": quoted_number, "username": "Unknown"}
                        )

            for jid in getattr(ctx_info, "mentionedJID", []):
                number = clean_number(jid.split("@")[0])
                try:
                    contact = client.contact.get_contact(number)
                    self.mentioned.append(
                        DynamicConfig(
                            {"number": number, "username": getattr(contact, "PushName", "Unknown")}
                        )
                    )
                except Exception:
                    self.mentioned.append(
                        DynamicConfig({"number": number, "username": "Unknown"})
                    )

    def build(self):
        self.urls = self.__client.utils.get_urls(self.content)
        raw_numbers = self.__client.utils.extract_numbers(self.content)
        self.numbers = [clean_number(n) for n in raw_numbers if n]

        if self.chat == "group":
            self.group = self.__client.get_group_info(self.gcjid)
            self.isAdminMessage = (
                self.sender.number
                in self.__client.filter_admin_users(self.group.Participants)
            )

        return self

    def raw(self):
        return self.__M
