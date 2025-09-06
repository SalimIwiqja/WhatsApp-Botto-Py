from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "stickerrename",
                "category": "tools",
                "aliases": ["sr", "take", "steal"],
                "description": {
                    "content": "Rename a sticker using the context or default name.",
                    "usage": "<name> | <packname>",
                },
                "exp": 2,
            },
        )

    def exec(self, M: MessageClass, contex):
        try:
            if not M.quoted:
                return self.client.reply_message(
                    f"🧩 *Please reply to a sticker* to rename it.\nUse: {self.client.config.prefix}stickerrename <name> | <packname>",
                    M,
                )

            media_type = self.client.detect_message_type(M.quoted)
            if media_type != "STICKER":
                return self.client.reply_message(
                    "❌ *This only works with stickers.* Please reply to a sticker message.",
                    M,
                )

            text = contex.text or ""
            parts = text.split("|")
            author = (
                parts[0].strip()
                if len(parts) > 0 and parts[0].strip()
                else f"Made by {M.sender.username}"
            )
            pack = (
                parts[1].strip()
                if len(parts) > 1 and parts[1].strip()
                else "Yuito"
            )

            sticker_media = self.client.download_any(M.quoted)

            self.client.send_sticker(
                M.gcjid, sticker_media, quoted=M, name=author, packname=pack
            )

        except Exception as e:
            self.client.reply_message(
                "⚠️ Failed to rename the sticker. Try again later.", M
            )
            self.client.log.error(f"[stickerrename] {e}")
