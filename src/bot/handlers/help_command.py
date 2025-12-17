"""This module contains the handler for the /help command in a Telegram bot. 
    When a user invokes the /help command, it sends a message listing the 
    available commands to the user.

Functions:
    handle_help_command(message: Message, bot: AsyncTeleBot) -> None: 
    Handles the /help command by sending a list of available commands to 
    the user.
"""
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

CMD = "help"

async def handle_help_command(message: Message, bot: AsyncTeleBot) -> None:
    """Handles the /help command by sending a list of available commands to the user.

    Args:
        message (Message): The message object that triggered the command.
        bot (AsyncTeleBot): The bot instance used to send the response.
    """
    help_message = (
        "👋 Olá\\!\n" 
        "🤖 Aqui está o que eu posso fazer por você:\n\n"
        "\\-/help : Você já está aqui\\! 📚\n\n"
        "\\- /tokens : Veja quantos tokens nós já processamos até agora\\! 📊\n\n"
        "\\- /info : Confira as configurações atuais do modelo Gemini que estou usando\\! 🧠✨\n\n"
        "\\- /blacklist : Veja a lista de URLs que eu não vou acessar\\! 🚫🕵️‍♂️\n\n"
        "\\- Basta me enviar uma mensagem com um ou mais links\\!\n\n"
        "Eu vou pegar o conteúdo e resumir para você\\! 🔗📋\n"
        "Precisa de mais alguma coisa\\? É só pedir\\! 😎"
    )

    await bot.send_message(
        message.chat.id, 
        help_message, 
        parse_mode="markdownv2")
