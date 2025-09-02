from libs import BaseCommand, MessageClass


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
            command = self.handler.commands.get(query) or next(
                (
                    cmd
                    for cmd in self.handler.commands.values()
                    if query in cmd.config.get("aliases", [])
                ),
                None,
            )

            if not command:
                return self.client.reply_message("❌ Command not found.", M)

            options = command.config
            if (
                M.sender.number not in self.client.config.mods
                and options.category == "dev"
            ):
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

        # Group all commands by category
        grouped = {}
        for cmd in self.handler.commands.values():
            cat = cmd.config.get("category", "Uncategorized").capitalize()
            grouped.setdefault(cat, []).append(cmd)

        emoji_array = ["🎎", "🔰", "🧑‍💻", "🍥", "🔊", "🎼", "🔍", "🧰"]
        category_names = sorted(grouped.keys())
        emoji_map = {
            cat: emoji_array[i % len(emoji_array)]
            for i, cat in enumerate(category_names)
        }

        header = f"""
> 🎫  *{self.client.config.name} Command List*  🎫

💡 *Prefix:* `{prefix}`

🎋 *Support us:* 
https://shorturl.at/WLhPG
""".strip()

        lines = [header]

        for cat in category_names:
            emoji = emoji_map.get(cat, "🔹")
            if M.sender.number not in self.client.config.mods and cat == "Dev":
                continue
            lines.append(f"\n> ━━━━❰ {emoji} *{cat.upper()}* {emoji} ❱━━━━\n")
            block = []
            for cmd in grouped[cat]:
                cfg = cmd.config
                desc = cfg.get("description", {})
                usage = desc.get("usage", "")
                formatted = f"{prefix}{self.client.utils.to_small_caps(cfg.command)} {self.client.utils.to_small_caps(usage)}".strip()
                block.append(formatted)
            lines.append("➨ ```" + ", ".join(block) + "```")

        lines.append(
            "\n📇 *Notes:*"
            "\n➪ Use `-help <command>` to view details."
            "\n➪ Example: `-help profile`"
            "\n➪ <> = required, [ ] = optional (omit brackets when typing)."
        )

        self.client.reply_message("\n".join(lines), M)
