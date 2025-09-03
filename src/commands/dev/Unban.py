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
                "devOnly": True,
            },
        )

    def exec(self, M: MessageClass, contex):
        # Permission check: dev OR mod
        if M.sender.number not in self.client.config.dev and M.sender.number not in self.client.config.mods:
            return self.client.reply_message(
                "⚠️ *Oops!* Some of these commands are *exclusively for developers or moderators*.", M
            )

        target = M.quoted_user or (M.mentioned[0] if M.mentioned else None)
        if not target:
            return self.client.reply_message("⚠️ Mention or quote someone to unban.", M)

        user_data = self.client.db.get_user_by_number(target.number)
        if not user_data or not user_data.ban:
            return self.client.reply_message(f"ℹ️ *@{target.number.split('@')[0]}* is *not banned*.", M)

        self.client.db.update_user_ban(target.number, False, "No ban")
        self.client.reply_message(f"🔓 *@{target.number.split('@')[0]}* has been *unbanned*.", M)
