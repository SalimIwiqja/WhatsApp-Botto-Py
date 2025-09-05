from libs import BaseCommand, MessageClass

def normalize_number(num):
    return num.replace("@c.us", "").replace("+", "")

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
                "devOnly": False,  # mods can also use
            },
        )

    def exec(self, M: MessageClass, contex):
        user_number = normalize_number(M.sender.number)
        dev_numbers = [normalize_number(n) for n in self.client.config.dev]
        mod_numbers = [normalize_number(n) for n in self.client.config.mods]

        if user_number not in dev_numbers + mod_numbers:
            return self.client.reply_message("⚠️ You don't have permission to use this command.", M)

        target = M.quoted_user or (M.mentioned[0] if M.mentioned else None)
        if not target:
            return self.client.reply_message("⚠️ Mention or quote someone to unban.", M)

        target_number = normalize_number(target.number)
        user_data = self.client.db.get_user_by_number(target_number)
        if not user_data or not user_data.ban:
            return self.client.reply_message(f"ℹ️ *@{target_number}* is not banned.", M)

        self.client.db.update_user_ban(target_number, False, "No ban")
        self.client.reply_message(f"🔓 *@{target_number}* has been unbanned.", M)
