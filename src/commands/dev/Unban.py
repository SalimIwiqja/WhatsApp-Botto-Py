from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "unban",
                "category": "group",
                "aliases": [],
                "description": {
                    "content": "Unban a previously banned user.",
                    "usage": "<@mention> or <quote>",
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

        target = M.quoted_user or (M.mentioned[0] if M.mentioned else None)
        if not target:
            return self.client.reply_message("⚠️ Mention or quote someone to unban.", M)

        # Normalize target number
        target_number = str(target.number).split("@")[0]

        user_data = self.client.db.get_user_by_number(target_number)
        if not user_data or not getattr(user_data, "ban", False):
            return self.client.reply_message(f"ℹ️ *@{target_number}* is not banned.", M)

        self.client.db.update_user_ban(target_number, False, "No ban")
        self.client.reply_message(f"🔓 *@{target_number}* has been unbanned.", M)
