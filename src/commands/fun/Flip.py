from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "coinflip",
                "category": "fun",
                "aliases": ["flip", "coin"],
                "description": {"content": "Flip a coin — heads or tails?"},
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        try:
            urls = [
                "https://media.tenor.com/Ud7b0YPvKFMAAAPo/coin-flip-coin-flip-tails.mp4",  # Heads sticker
                "https://media.tenor.com/ncCwrdZ6UWsAAAPo/coin-flip-coin-flip-heads.mp4",  # Tails sticker
            ]
            selected_url = self.client.utils.get_random_item(urls)

            buffer = self.client.utils.fetch_buffer(selected_url)
            self.client.send_sticker(
                M.gcjid, buffer, quoted=M, name="Created by", packname="Yuito"
            )

        except Exception as e:
            self.client.reply_message("⚠️ Failed to flip the coin.", M)
            self.client.log.error(f"[CoinFlipError] {e}")
