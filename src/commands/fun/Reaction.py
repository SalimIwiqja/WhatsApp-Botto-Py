from libs import BaseCommand, MessageClass, get_push_name

REACTIONS = {
    "bite": "Bit",
    "blush": "Blushed at",
    "bonk": "Bonked",
    "bully": "Bullied",
    "cringe": "Cringed at",
    "cry": "Cried in front of",
    "cuddle": "Cuddled",
    "dance": "Danced with",
    "glomp": "Glomped at",
    "handhold": "Held the hands of",
    "happy": "is Happied with",
    "highfive": "High-fived",
    "hug": "Hugged",
    "kick": "Kicked",
    "kill": "Killed",
    "kiss": "Kissed",
    "lick": "Licked",
    "nom": "Nomed",
    "pat": "Patted",
    "poke": "Poked",
    "slap": "Slapped",
    "smile": "Smiled at",
    "smug": "Smugged",
    "wave": "Waved at",
    "wink": "Winked at",
    "yeet": "Yeeted at",
}

REACTION_ALIASES = list(REACTIONS.keys())


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "reaction",
                "aliases": ["r"] + REACTION_ALIASES,
                "category": "fun",
                "description": {
                    "content": "React with a gif to someone.",
                    "usage": "<reaction> <@mention> | <quote>",
                },
                "exp": 5,
            },
        )

    def exec(self, M: MessageClass, contex):
        cmd = contex.cmd.lower()
        text = contex.text.strip() if contex.text else ""
        raw_mode = cmd not in ("reaction", "r")

        # Determine reaction
        reaction = cmd if raw_mode else text.split(" ")[0].lower()
        if not raw_mode and not text:
            usage = "\n- " + "\n- ".join(r.capitalize() for r in REACTIONS.keys())
            return self.client.reply_message(
                f"🎃 *Available Reactions:*\n{usage}\n\n🛠️ *Usage:* {self.client.config.prefix}reaction <type> [tag or quote user]\nExample: {self.client.config.prefix}pat",
                M,
            )

        if reaction not in REACTIONS:
            return self.client.reply_message(
                f"❌ Invalid reaction. Use *{self.client.config.prefix}reaction* to view available options.",
                M,
            )

        try:
            target = M.quoted_user or (M.mentioned[0] if M.mentioned else M.sender)
            single = target == M.sender

            api_data = self.client.utils.fetch(f"https://api.waifu.pics/sfw/{reaction}")
            gif_url = api_data["url"]
            gif_buffer = self.client.utils.fetch_buffer(gif_url)

            caption = f"*@{M.sender.number} {REACTIONS[reaction]}* "
            caption += "*themselves*" if single else f"*@{target.number}*"

            self.client.send_video(
                M.gcjid,
                gif_buffer,
                caption=caption,
                quoted=M,
                gifplayback=True,
                is_gif=True,
            )

        except Exception as e:
            self.client.reply_message("⚠️ Failed to send reaction.", M)
            self.client.log.error(f"[ReactionError] {e}")
