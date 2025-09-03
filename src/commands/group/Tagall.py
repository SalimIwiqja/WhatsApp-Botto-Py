from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "tagall",
                "category": "group",
                "aliases": ["everyone"],
                "description": {
                    "content": "Tag all group members.",
                    "usage": "[optional message]",
                },
                "exp": 1,
                "group": True,
                "adminOnly": True,
            },
        )

    def exec(self, M: MessageClass, contex):
        if not M.sender.is_admin:
            return self.client.reply_message("❌ You must be a group admin to use this command.", M)

        members = self.client.get_group_members(M.chat)
        if not members:
            return self.client.reply_message("⚠️ Could not fetch group members.", M)

        message_text = contex.text.strip() if contex.text else ""
        tagged_mentions = [f"@{m.number.split('@')[0]}" for m in members if m.number != self.client.user.number]

        if not tagged_mentions:
            return self.client.reply_message("⚠️ No members to tag.", M)

        full_message = message_text + "\n\n" + " ".join(tagged_mentions)
        try:
            self.client.send_message(
                M.chat,
                full_message,
                mentions=[m.number for m in members if m.number != self.client.user.number]
            )
        except Exception as e:
            return self.client.reply_message(f"❌ Failed to tag members.\nError: {str(e)}", M)
