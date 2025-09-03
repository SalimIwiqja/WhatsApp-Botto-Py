from libs import BaseCommand, MessageClass

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
                "devOnly": False,  # allow mods too
            },
        )

    def exec(self, M: MessageClass, contex):
        user_number = M.sender.number
        # check if sender is dev or mod
        if user_number not in self.client.config.dev and user_number not in self.client.config.mods:
            return self.client.reply_message("⚠️ You don't have permission to use this command.", M)

        text = contex.text.strip()
        target = M.quoted_user or (M.mentioned[0] if M.mentioned else None)
        if not target:
            return self.client.reply_message("⚠️ Mention or quote someone to ban.", M)

        parts = text.split("|", 1)
        reason = parts[1].strip() if len(parts) > 1 else "No reason provided."

        user_data = self.client.db.get_user_by_number(target.number)
        if user_data and user_data.ban:
            return self.client.reply_message(
                f"⚠️ *@{target.number.split('@')[0]}* is already banned.\n📝 Reason: {user_data.reason}", M
            )

        self.client.db.update_user_ban(target.number, True, reason)
        self.client.reply_message(
            f"🔒 *@{target.number.split('@')[0]}* has been banned.\n📝 Reason: {reason}", M
        )
