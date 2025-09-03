from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "unban",
                "category": "dev",
                "aliases": [],
                "description": {
                    "content": "Unban a previously banned user.",
                    "usage": "<@mention> | <quote>",
                },
                "exp": 0,
                "group": True,
                "devOnly": False,  # Allow mods too
            },
        )

    def exec(self, M: MessageClass, contex):
        sender = M.sender.number.split('@')[0]
        allowed = [n.split('@')[0] for n in self.client.config.dev + self.client.config.mods]
        if sender not in allowed:
            return self.client.reply_message(
                "⚠️ You don't have permission to use this command.", M
            )

        target = M.quoted_user or (M.mentioned[0] if M.mentioned else None)
        if not target:
            return self.client.reply_message("⚠️ Mention or quote someone to unban.", M)

        user_data = self.client.db.get_user_by_number(target.number)
        if not user_data or not user_data.ban:
            return self.client.reply_message(f"ℹ️ *@{target.number.split('@')[0]}* is *not banned*.", M)

        self.client.db.update_user_ban(target.number, False, "No ban")
        self.client.reply_message(f"🔓 *@{target.number.split('@')[0]}* has been *unbanned*.", M)
