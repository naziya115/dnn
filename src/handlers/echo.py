from aiogram import Router, F
from aiogram.types import Message


router: Router = Router()


# @router.message(
#     F.content_type.in_(
#         [
#             "text", "audio", "voice",
#             "sticker", "document", "photo",
#             "video"
#         ]
#     )
# )
# async def echo(message: Message) -> None:
#     text =
#     await message.bot.send_message(chat_id=-1002352092101, text=message.text)