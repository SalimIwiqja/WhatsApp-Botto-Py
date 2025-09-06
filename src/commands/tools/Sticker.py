from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "sticker",
                "category": "tools",
                "aliases": ["s"],
                "description": {
                    "content": "Create sticker from an image or video",
                    "usage": "<name> | <packname>",
                },
                "exp": 3,
            },
        )

    def exec(self, M: MessageClass, contex):
        try:
            author, pack = "Created by", "Yuito"
            if contex.text:
                parts = [part.strip() for part in contex.text.split("|", 1)]
                if parts:
                    author = parts[0] or author
                    if len(parts) > 1:
                        pack = parts[1] or pack

            source = M.quoted or M.Message
            media = self.client.download_any(source)
            media_type = self.client.detect_message_type(source)

            if media_type not in ("IMAGE", "VIDEO"):
                return self.client.reply_message(
                    f"🖼️ *Please send an image, video, or GIF* with the caption *{self.client.config.prefix}sticker*, or reply to a media message using *{self.client.config.prefix}sticker*.",
                    M,
                )

            self.client.send_sticker(
                M.gcjid, media, quoted=M, name=author, packname=pack
            )

        except Exception as e:
            self.client.reply_message(
                "❌ Failed to create sticker. Please try again.", M
            )
            self.client.log.error(f"[sticker] {e}")
