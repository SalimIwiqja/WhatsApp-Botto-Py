from libs import BaseCommand, MessageClass
import requests
from io import BytesIO

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "help",
                "category": "core",
                "aliases": ["h"],
                "description": {
                    "content": "Show all commands or help for a specific one.",
                    "usage": "<command>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        prefix = self.client.config.prefix
        query = contex.text.strip().lower() if contex.text else None

        if query:
            # Single command help
            command = self.handler.commands.get(query) or next(
                (cmd for cmd in self.handler.commands.values() if query in cmd.config.get("aliases", [])),
                None,
            )
            if not command:
                return self.client.reply_message("❌ Command not found.", M)

            options = command.config
            if M.sender.number not in self.client.config.mods and options.category == "dev":
                return self.client.reply_message("❌ Command not found.", M)

            desc = options.get("description", {})
            aliases = ", ".join(options.get("aliases", [])) or "No aliases"
            usage = f"{prefix}{options.command} {desc.get('usage', '')}".strip()
            content = desc.get("content", "No description available")

            help_text = f"""\
🔰 *Command:* {options.command}
🔁 *Aliases:* {aliases}
ℹ️ *Category:* {options.category.capitalize()}
⚙️ *Usage:* {usage}
📝 *Description:* {content}
"""
            return self.client.reply_message(help_text, M)

        # Full help menu
        grouped = {}
        for cmd in self.handler.commands.values():
            cat = cmd.config.get("category", "Uncategorized").capitalize()
            grouped.setdefault(cat, []).append(cmd)

        # Assign emojis to categories
        emoji_array = ["🎎", "🔰", "🧑‍💻", "🍥", "🔊", "🎼", "🔍", "🧰"]
        category_names = sorted(grouped.keys())
        emoji_map = {cat: emoji_array[i % len(emoji_array)] for i, cat in enumerate(category_names)}

        # Header
        header = f"""
> 🎫  *{self.client.config.name} Command List*  🎫

💡 *Prefix:* `{prefix}`

🎋 *Support us:* 
https://shorturl.at/WLhPG
""".strip()

        lines = [header]

        # Categories
        for cat in category_names:
            emoji = emoji_map.get(cat, "🔹")
            if M.sender.number not in self.client.config.mods and cat == "Dev":
                continue
            # Add spacing before category
            lines.append(f"\n> ━━━━❰ {emoji} *{cat.upper()}* {emoji} ❱━━━━\n")
            block = []
            for cmd in grouped[cat]:
                cfg = cmd.config
                desc = cfg.get("description", {})
                usage = desc.get("usage", "")
                formatted = f"{prefix}{self.client.utils.to_small_caps(cfg.command)} {self.client.utils.to_small_caps(usage)}".strip()
                block.append(formatted)
            # Commands one per line inside monospace
            lines.append("➨ ```\n" + "\n".join(block) + "\n```")

        # Notes section
        lines.append(
            "\n📇 *Notes:*"
            "\n➪ Use `-help <command>` to view details."
            "\n➪ Example: `-help profile`"
            "\n➪ <> = required, [ ] = optional (omit brackets when typing)."
        )

        final_text = "\n".join(lines)

        # Send image from your Catbox link with help text as caption
        image_url = "https://files.catbox.moe/qjtp8v.jpg"
        try:
            resp = requests.get(image_url)
            if resp.status_code == 200:
                image_bytes = BytesIO(resp.content)
                self.client.send_image(M.gcjid, image_bytes, caption=final_text)
            else:
                self.client.reply_message(final_text, M)
        except Exception as e:
            self.client.log.error(f"[HelpImageError] {e}")
            self.client.reply_message(final_text, M)
