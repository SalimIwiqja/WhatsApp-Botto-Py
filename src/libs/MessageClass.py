from libs import Void
from utils import DynamicConfig
from neonize.events import MessageEv
import re

class MessageClass:
    def __init__(self, client: Void, message: MessageEv):
        self.__client = client
        self.__M = message

        self.Info = message.Info
        self.Message = message.Message
        self.content = client.extract_text(self.Message)
        self.gcjid = self.Info.MessageSource.Chat
        self.chat = "group" if self.Info.MessageSource.IsGroup else "dm"

        # Normalize sender number
        sender_number = self.normalize_number(self.Info.MessageSource.Sender.User)
        sender_contact = client.contact.get_contact(client.build_jid(sender_number))
        self.sender = DynamicConfig(
            {
                "number": sender_number,
                "username": sender_contact.PushName if sender_contact else sender_number,
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
                    quoted_number = self.normalize_number(ctx_info.participant)
                    quoted_contact = client.contact.get_contact(client.build_jid(quoted_number))
                    self.quoted_user = DynamicConfig(
                        {
                            "number": quoted_number,
                            "username": quoted_contact.PushName if quoted_contact else quoted_number,
                        }
                    )

            # Handle mentioned users
            for jid in ctx_info.mentionedJID:
                number = self.normalize_number(jid)
                contact = client.contact.get_contact(client.build_jid(number))
                self.mentioned.append(
                    DynamicConfig(
                        {
                            "number": number,
                            "username": contact.PushName if contact else number,
                        }
                    )
                )

    def build(self):
        self.urls = self.__client.utils.get_urls(self.content)
        self.numbers = self.__client.utils.extract_numbers(self.content)

        if self.chat == "group":
            self.group = self.__client.get_group_info(self.gcjid)
            admins = self.__client.filter_admin_users(self.group.Participants)
            self.isAdminMessage = self.sender.number in admins

        return self

    def raw(self):
        return self.__M

    def normalize_number(self, number: str) -> str:
        """
        Normalize WhatsApp numbers:
        - Remove any extra characters like trailing dots
        - Remove '@s.whatsapp.net' if present
        - Ensure only digits with optional '+' at start
        """
        if not number:
            return ""
        # Remove trailing dots or spaces
        number = number.strip().rstrip(".")
        # Remove domain part
        number = re.sub(r"@.*$", "", number)
        # Remove non-digit characters except leading '+'
        if number.startswith("+"):
            number = "+" + re.sub(r"[^\d]", "", number)
        else:
            number = re.sub(r"[^\d]", "", number)
        return number
