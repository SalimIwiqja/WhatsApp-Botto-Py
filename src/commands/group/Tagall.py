from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "tagall",
                "category": "group",
                "aliases": ["all"],
                "description": {
                    "content": "Mention all members in the group.",
                    "usage": "",
                },
                "exp": 5,
                "group": True,
                "devOnly": False,
            },
        )

    def exec(self, M: MessageClass, contex):
        # Ensure this is a group
        if M.chat != "group":
            return self.client.reply_message(
                "⚠️ This command can only be used in a group.", M
            )

        # Get group participants
        group = M.group
        if not group or not hasattr(group, "Participants"):
            return self.client.reply_message(
                "⚠️ Failed to get group info. No participants found.", M
            )

        mentions = []
        text = "📢 Attention everyone!\n\n"

        for p in group.Participants:
            # Get the user number safely
            number = getattr(p.JID, "User", None)
            if not number:
                continue  # skip if no valid number
            mentions.append(number)
            text += f"@{number} "

        # Send the message with mentions
        self.client.send_message(M.gcjid, text.strip(), mentions=mentions)
