from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "tagall",
                "category": "group",
                "aliases": ["mentionall", "ta"],
                "description": {
                    "content": "Mention all group members.",
                    "usage": "<optional_text>",
                },
                "group": True,
                "admin": True,
                "exp": 0,
            },
        )

    def exec(self, M: MessageClass, contex):
        try:
            participants = M.group.Participants
            if not participants:
                return self.client.reply_message(
                    "⚠️ Could not fetch *participant list*.", M
                )

            mentions = []
            tags = []

            for member in participants:
                # Skip the bot itself
                if member.JID.User != self.client.get_me().JID.User:
                    mentions.append(member.JID)  # full JID for actual mention
                    tags.append(f"@{member.JID.User}")  # show number as text

            prefix_text = (
                contex.text.strip()
                if contex.text
                else "📢 *Attention everyone!*"
            )
            message = f"{prefix_text}\n\n" + " ".join(tags)

            # Send message with proper mentions
            self.client.send_message(
                M.gcjid,
                message,
                mentions=mentions
            )

        except Exception as e:
            self.client.reply_message(
                "❌ An error occurred while tagging everyone.", M
            )
            self.client.log.error(f"[TagAllError] {e}")
