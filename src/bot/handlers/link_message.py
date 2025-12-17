"""This module contains the implementation for handling messages that contain 
    URLs in a Telegram bot. It includes an asynchronous function to process 
    incoming messages, extract URLs, crawl them for content, and respond to 
    the user with generated text and links to articles. Has a separate function
    to handle messages that do not contain any URLs.

Functions:
    handle_link_message(message: Message, bot: AsyncTeleBot) -> None:
        Handles messages containing URLs by extracting and processing the links.
    handle_no_link_message(message: Message, bot: AsyncTeleBot) -> None:
        Handles messages that do not contain any URLs.
"""
from enum import Enum

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from crawler import crawl_urls, ScrapeResult
from gemini import GeminiAPIClient, GeminiResponse
from utils import link_utils, markdown_v2_sanitizer

from ..bot_utils import message_markup


class ErrorMessages(Enum):
    """Contains error messages for the link message handler."""
    NO_VALID_URLS_MESSAGE = (
        "Ops\\! 🤖 Não encontrei nenhuma URL válida na sua mensagem\\." 
        "📭 Mande um link e deixe a mágica acontecer\\! ✨"
    )

    CANNOT_CRAWL_MESSAGE = (
        "Ops\\! 🕵️‍♂️ Nosso detetive da web tropeçou num link quebrado\\! "
        "Tente outro link ou verifique se o site está no ar\\! 🌐💥"
    )

    GEMINI_API_FAIL_REASON_MESSAGE = (
        "Eita\\! 🚨 O Gemini parou porque: _{reason}_\n"
        "Parece que algo assustou ele\\! 😬 "
        "Vamos tentar de novo com calma\\! 😊"
    )

    GEMINI_API_FAIL_MESSAGE = (
        "Uh\\-oh\\! 🚧 O Gemini ficou mudo por motivos desconhecidos\\… "
        "Talvez os astros estejam desalinhados\\? 🌠 Vamos tentar de novo\\!"
    )

    NO_LINK_MESSAGE = (
        "Ops\\! 🤖 Parece que não tem nenhum link na sua mensagem\\." 
        "📭 Mande um link e deixe a mágica acontecer\\! ✨"
    )
    def format(self, *args, **kwargs) -> str:
        """Formats the error message with the given arguments."""
        return self.value.format(*args, **kwargs)

async def handle_link_message(message: Message, bot: AsyncTeleBot) -> None:
    """Handles messages containing URLs by extracting and processing the links.

    This asynchronous function performs the following tasks:
        1. Extracts URLs from the incoming text message.
        2. Crawls the extracted URLs to scrape their content and sub-links.
        3. Generates a text response based on the scraped content using 
            the Gemini API.
        4. Replies to the user with the generated text, including a button 
            linking to the original article.

    Args:
        message (Message): The incoming Telegram message containing the URLs.
        bot (AsyncTeleBot): The bot instance used to send the reply message.

    Returns:
        None: This function does not return a value.
    """
    # Utility function to reply with a message indicating that no valid URLs
    async def reply_with_error(response_text: str) -> None:
        return await bot.reply_to(
            message,
            response_text,
            parse_mode="markdownv2",
            disable_notification=True
        )

    # show GemDigest is typing on the chat top bar
    await bot.send_chat_action(message.chat.id, "typing")

    urls = link_utils.extract_urls(message.text)
    if not urls:
        return await reply_with_error(
            ErrorMessages.NO_VALID_URLS_MESSAGE.value)
            
    scrape_results: list[ScrapeResult] = await crawl_urls(urls)
    if not scrape_results:
        return await reply_with_error(ErrorMessages.CANNOT_CRAWL_MESSAGE.value)
    
    for result in scrape_results:
        prompt = result.content + "\n\n" + "\n".join(result.sub_urls)
        output: GeminiResponse = await GeminiAPIClient.generate_text(prompt)

        if not output.text or output.error_message:
            error_message = (
                ErrorMessages.GEMINI_API_FAIL_MESSAGE.value 
                if not output.error_message 
                else ErrorMessages.GEMINI_API_FAIL_REASON_MESSAGE.format(
                    reason=markdown_v2_sanitizer.sanitize_str(output.error_message))
            )
            await reply_with_error(error_message)
        else:
            await bot.reply_to(
                message,
                output.text if output.text else output.error_message,
                disable_notification=True,
                parse_mode='html',
                reply_markup=message_markup.generate_article_button_markup(
                    result.original_url)
            )


async def handle_no_link_message(message: Message, bot: AsyncTeleBot) -> None:
    """Handles messages that do not contain any URLs.

    This asynchronous function replies to the user with a message indicating 
    that no URLs were found in the incoming message.

    Args:
        message (Message): The incoming Telegram message without any URLs.
        bot (AsyncTeleBot): The bot instance used to send the reply message.

    Returns:
        None: This function does not return a value.
    """

    await bot.reply_to(
        message,
        ErrorMessages.NO_LINK_MESSAGE.value,
        parse_mode="markdownv2",
        disable_notification=True
    )
