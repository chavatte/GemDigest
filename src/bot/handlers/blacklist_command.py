from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from configs.website_blacklist import blacklisted_websites 
from utils.markdown_v2_sanitizer import sanitize_str

CMD = "blacklist"

_formatted_blacklisted_urls = [
    f"🚷 _{_id}\\._ `{sanitize_str(url)}`\n"
    for _id, url in enumerate(blacklisted_websites)]


async def handle_blacklist_command(message: Message, bot: AsyncTeleBot) -> None:

    blacklist_message = (
        "🚫 _Blacklist na Área\\!_ 🚫\n"
        "Estes são os sites complicados que o bot não vai acessar "
        "\\(nada de espiar por aqui\\!\\) 🕵️‍♂️❌:\n\n"
        f"{''.join(_formatted_blacklisted_urls)}"
        "\n"
        "_O bot sabe onde não deve ir\\! Navegando com segurança "
        "e evitando as zonas proibidas da web\\!_ 🕸️💨"
    )

    await bot.send_message(
        message.chat.id, 
        blacklist_message, 
        parse_mode="markdownv2")
