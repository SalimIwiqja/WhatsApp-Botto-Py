from libs import BaseCommand, MessageClass
from libs.MessageClass import get_push_name

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "ban",
                "category": "group",
                "aliases": [],
                "description": {
                    "content": "Ban a user from using the bot.",
                    "usage": "<@mention> or <quote> | <reason>",
                },
                "exp": 0,
                "group": True,
                "devOnly": False,  # mods can also use
            },
        )

    def exec(self, M: MessageClass, contex):
        user_number = M.sender.number
        dev_numbers = [n for n in self.client.config.dev]
        mod_numbers = [n for n in self.client.config.mods]

        if user_number not in dev_numbers + mod_numbers:
            return self.client.reply_message(
                "⚠️ You don't have permission to use this command.", M
            )

        target = M.quoted_user or (M.mentioned[0] if M.mentioned else None)
        if not target:
            return self.client.reply_message("⚠️ Mention or quote someone to ban.", M)

        parts = contex.text.strip().split("|", 1)
        reason = parts[1].strip() if len(parts) > 1 else "No reason provided."

        target_number = target.number
        user_data = self.client.db.get_user_by_number(target_number)
        if user_data and user_data.ban:
            return self.client.reply_message(
                f"⚠️ *@{target_number}* is already banned.\n📝 Reason: {user_data.reason}", M
            )

        self.client.db.update_user_ban(target_number, True, reason)
        self.client.reply_message(
            f"🔒 *@{target_number}* has been banned.\n📝 Reason: {reason}", M
        )
