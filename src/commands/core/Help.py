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
            # Single command help (keep old behavior)
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

        # Full help menu (Nexus Style)
        help_text = f"""⛩️❯─「 *Nexus Inc* 」─❮⛩️

🌸 *Konnichiwaaa* (๑>ᴗ<๑) @{M.sender.username or M.sender.number.split('@')[0]}
I'm *Yuito* ✨
🍀 My prefix is *"{prefix}"* ~

*📭 Command List 📭*

❯──── Anime ────❮
➠```#aid, #anime, #character, #cid, #husbu, #kitsune, #manga, #mid, #neko, #waifu```

❯──── Core ────❮
➠```#blocklist, #groupinfo, #help, #hi, #info, #leaderboard, #mods, #whoami, #rank```

❯──── Dev ────❮
➠```#ban, #broadcast, #disable, #enable, #eval, #unban```

❯──── Fun ────❮
➠```#advice, #animal, #charactercheck, #fact, #coinflip, #pick, #reaction, #ship```

❯──── Group ────❮
➠```#add, #demote, #groupannounce, #groupeditlock, #grouplink, #promote, #remove, #setdesc, #setname, #setphoto, #tagall, #toggle```

❯──── Media ────❮
➠```#play, #ytaudio, #ytsearch, #ytvideo```

❯──── Search ────❮
➠```#gif, #github, #gsearch, #iplookup, #weather, #urban```

❯──── Tools ────❮
➠```#emojimix, #emojisticker, #sticker, #stickerrename```

📝 *Hint:* Use *#help <command_name>* for detailed info!  
🌟 *Arigato for Choosing Nexus!* 🌟
"""

        # Catbox banner image
        image_url = "https://raw.githubusercontent.com/SalimIwiqja/WhatsApp-Botto-Py/refs/heads/main/src/Scarlet-Nexus-Anime-3.jpg"
try:
    resp = requests.get(image_url, timeout=10)
    if resp.status_code == 200:
        image_bytes = BytesIO(resp.content)
        self.client.send_image(M.gcjid, image_bytes, caption=final_text)
    else:
        self.client.reply_message(final_text, M)
except Exception as e:
    self.client.log.error(f"[HelpImageError] {e}")
    self.client.reply_message(final_text, M)
