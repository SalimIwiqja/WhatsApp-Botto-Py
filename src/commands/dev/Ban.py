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
        # Normalize sender number
        user_number = M.sender.number.split("@")[0]

        # Check if sender is dev or mod
        if user_number not in self.client.config.dev and user_number not in self.client.config.mods:
            return self.client.reply_message("⚠️ You don't have permission to use this command.", M)

        text = contex.text.strip()
        target = M.quoted_user or (M.mentioned[0] if M.mentioned else None)
        if not target:
            return self.client.reply_message("⚠️ Mention or quote someone to ban.", M)

        # Normalize target number
        target_number = str(target.number).split("@")[0]

        # Split reason
        parts = text.split("|", 1)
        reason = parts[1].strip() if len(parts) > 1 else "No reason provided."

        user_data = self.client.db.get_user_by_number(target_number)
        if user_data and getattr(user_data, "ban", False):
            return self.client.reply_message(
                f"⚠️ *@{target_number}* is already banned.\n📝 Reason: {getattr(user_data, 'reason', 'No reason')}", M
            )

        self.client.db.update_user_ban(target_number, True, reason)
        self.client.reply_message(
            f"🔒 *@{target_number}* has been banned.\n📝 Reason: {reason}", M
        )
