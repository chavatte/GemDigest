from telebot.types import ChatMemberUpdated
from telebot.async_telebot import AsyncTeleBot

from configs import api_keys

_admin_ids = api_keys.get_admin_user_ids()

async def handle_chat_join(
    chat_member_updated: ChatMemberUpdated, 
    bot: AsyncTeleBot
) -> None:
    """ Handle the bot joining a chat.
    """
    added_by_user_id = chat_member_updated.from_user.id

    if not added_by_user_id in _admin_ids:
        # Leave the chat if the bot was not added by an admin
        return await bot.leave_chat(chat_member_updated.chat.id)

    chat_join_message = (
        "👋 Olá pessoal\\!\n"
        "Eu sou o *GemDigest* 🤖, seu bot prático para transformar artigos longos "
        "em resumos rápidos\\. Basta compartilhar um link de um artigo, "
        "e eu trarei os destaques num piscar de olhos\\! 📰✨\n\n"
        "Precisa de mais informações? Digite /help para ver como posso ajudar\\. "
        "Deixe-me ajudar a economizar tempo e ir direto ao ponto\\. 🎯\n"
        "Mande um link e vamos começar\\! 📝🔗"
    )

    # is one of "member", "administrator" or "left"
    bot_status = chat_member_updated.new_chat_member.status
    chat_member_updated.new_chat_member.status

    if bot_status == "member":
        await bot.send_message(
            chat_member_updated.chat.id,
            chat_join_message,
            parse_mode="markdownv2",
            disable_notification=True
        )


async def handle_member_joined(
    chat_member_updated: ChatMemberUpdated, 
    bot: AsyncTeleBot
) -> None:

    user_name = chat_member_updated.new_chat_member.user.username

    chat_join_message = (
        f"👋 Bem\\-vindo(a), {user_name}\\!\n"
        "Eu sou o GemDigest, o bot aqui para te ajudar a ficar por dentro "
        "dos últimos artigos sem precisar ler tudo\\! 📚✨ "
        "Basta compartilhar um link e eu te envio um resumo rápido\\.\n\n"
        "Precisa de mais informações? Digite /help para ver como posso ajudar\\. "
        "Ansioso para te fazer economizar tempo\\! "
        "Mande um link sempre que quiser um resumo\\. 📰🔗"
    )

    # is one of "member", "administrator" or "left"
    bot_status = chat_member_updated.new_chat_member.status
    chat_member_updated.new_chat_member.status

    if bot_status == "member":
        await bot.send_message(
            chat_member_updated.chat.id,
            chat_join_message,
            parse_mode="markdownv2",
            disable_notification=True
        )
