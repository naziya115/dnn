import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config, load_config
from src.handlers import echo, commands

from src.adapters import npr_parser, bbc, test

logger = logging.getLogger(__name__)

config: Config = load_config()

bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher()

async def bbc_periodic_post():
    links = list()
    big_arr = set()
    general_prompt = """Summarize the following article. Ensure the summary accurately conveys all key points from the original text without omitting crucial details or introducing new interpretations. Use clear, concise, and neutral language. Highlight essential keywords in bold where necessary. Limit the summary to a maximum of 500 characters.."""
    while True:
        if not links:
            links = list(bbc.get_all_links("https://www.bbc.com/news/world"))
            for link in links[:]:
                if link in big_arr:
                    links.remove(link)
            await asyncio.sleep(5)
        else:
            for link in links:
                title = bbc.get_title(link)
                text = bbc.get_article_text(link)
                image = bbc.get_image(link)
                if title:
                    prompt = title + "\n" + text + "\n" + general_prompt
                else:
                    prompt = text + "\n Summarize this text"
                try:
                    response = test.post_request_kazllm(prompt)['vllm_response']['content']
                    print(response)
                    translation = test.translate_text(response)
                    print(translation)
                except Exception as e:
                    print(f"Failed to send message: {e}")
                    continue

                try:
                    translation_text = translation['text']

                    caption = translation_text[:1024]
                    remaining_text = translation_text[1024:]

                    await bot.send_photo(chat_id=-1002352092101, photo=image, caption=caption)

                    if remaining_text:
                        chunks = [remaining_text[i:i + 4096] for i in range(0, len(remaining_text), 4096)]
                        for chunk in chunks:
                            chunk = "Алдыңғы жазбаның жалғасы\n\n" + chunk
                            await bot.send_message(chat_id=-1002352092101, text=chunk)
                except Exception as e:
                    print(f"Failed to send message: {e}")
                await asyncio.sleep(60)
            big_arr.update(set(links))
            links = list()


async def npr_periodic_post():
    links = list()
    big_arr = set()
    general_prompt = """Summarize the following article. Ensure the summary accurately conveys all key points from the original text without omitting crucial details or introducing new interpretations. Use clear, concise, and neutral language. Highlight essential keywords in bold where necessary. Limit the summary to a maximum of 500 characters.."""
    while True:
        if not links:
            links = list(npr_parser.get_links("https://www.npr.org/"))
            print(links)
            for link in links[:]:
                if link in big_arr:
                    links.remove(link)
            await asyncio.sleep(5)
        else:
            for link in links:
                content = npr_parser.get_text(link)
                title = content["title"]
                text = content["content"]
                image = content["image_url"]
                if title:
                    prompt = title + "\n" + text + "\n" + general_prompt
                else:
                    prompt = text + "\n Summarize this text"
                try:
                    response = test.post_request_kazllm(prompt)['vllm_response']['content']
                    print(11111111, response)
                    translation = test.translate_text(response)
                    print(11111111, translation)
                except Exception as e:
                    print(f"Failed to send message: {e}")
                    continue

                try:
                    translation_text = translation['text']

                    caption = translation_text[:1024]
                    remaining_text = translation_text[1024:]

                    await bot.send_photo(chat_id=-1002352092101, photo=image, caption=caption)

                    if remaining_text:
                        chunks = [remaining_text[i:i + 4096] for i in range(0, len(remaining_text), 4096)]
                        for chunk in chunks:
                            chunk = "Алдыңғы жазбаның жалғасы\n\n" + chunk
                            await bot.send_message(chat_id=-1002352092101, text=chunk)
                except Exception as e:
                    print(f"Failed to send message: {e}")
                await asyncio.sleep(60)
            big_arr.update(set(links))
            links = list()




async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    dp.include_router(echo.router)
    dp.include_router(commands.router)

    asyncio.create_task(bbc_periodic_post())
    asyncio.create_task(npr_periodic_post())
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:

        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")


