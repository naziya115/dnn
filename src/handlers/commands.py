from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile, InputFile
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext


from src.adapters import bbc, test, base64_to_audio
from src.states.states import MainState

router = Router()

import os

# audio_path = "E:/Nariman/dnn hackathon/aiogram-bot-template/output.mp3"
# if os.path.exists(audio_path):
#     print("ЕСТЬ")
# else:
#     print("НЕТ")


@router.message(Command("start"))
async def search_interlocutor(message: Message) -> None:
    await message.bot.send_message(chat_id=message.from_user.id, text="BBC мақаласын аудару үшін /bbc_article жазыңыз.\nНемесе мәтіннің дұрыстығын тексеру үшін /grammar_check поштасына жіберіңіз.\n/get_article_audio")

@router.message(Command("bbc_article"))
async def search_interlocutor(message: Message, state: FSMContext) -> None:
    await message.bot.send_message(chat_id=message.from_user.id, text="Сілтемені келесі хабарламамен жіберіңіз.\nБасқа ештеңе жібермеңіз. ")
    await state.set_state(MainState.link)

@router.message(MainState.link)
async def private_chat_summary(message: Message, state: FSMContext) -> None:
    link = message.text
    title = bbc.get_title(link)
    text = bbc.get_article_text(link)
    image = bbc.get_image(link)
    general_prompt = """Summarize the following article. Ensure the summary captures the key points from the original 
    text without adding, removing, or interpreting any information. Use clear and concise language. Do not include 
    any personal opinions or assumptions."""

    if title:
        prompt = title + "\n" + text + "\n" + general_prompt
    else:
        prompt = text + "\n" + general_prompt
    try:
        response = test.post_request_kazllm(prompt)['vllm_response']['content']
        translation = test.translate_text(response)
    except:
        await message.bot.send_message(chat_id=message.from_user.id, text="На данный момент, к сожалению, мы не можем обработать эту статью")
    try:
        translation_text = translation['text']

        caption = translation_text[:1024]
        remaining_text = translation_text[1024:]

        await message.bot.send_photo(chat_id=message.from_user.id, photo=image, caption=caption)

        if remaining_text:
            chunks = [remaining_text[i:i + 4096] for i in range(0, len(remaining_text), 4096)]
            for chunk in chunks:
                chunk = "Алдыңғы жазбаның жалғасы\n\n" + chunk
                await message.bot.send_message(chat_id=message.from_user.id, text=chunk)
    except Exception as e:
        print(f"Failed to send message: {e}")

    await state.clear()


@router.message(Command("grammar_check"))
async def grammar_check(message: Message, state: FSMContext) -> None:
    await message.bot.send_message(chat_id=message.from_user.id, text="Грамматикалық тұрғыдан тексерілетін мәтінді жіберіңіз ")
    await state.set_state(MainState.grammar_check)


@router.message(MainState.grammar_check)
async def grammar_check_response(message: Message, state: FSMContext) -> None:
    general_prompt = """Мәтіннің грамматикасын тексеріңіз. Қажет болса, түзетулер енгізіңіз және түзетілген мәтінді көрсетіңіз."""

    prompt = message.text + "\n" + general_prompt

    try:
        response = test.post_request_kazllm(prompt)['vllm_response']['content']
    except:
        await message.bot.send_message(chat_id=message.from_user.id,
                                       text="Упс, что то пошло не так")

    await message.bot.send_message(chat_id=message.from_user.id,
                                   text=response)

    await state.clear()


@router.message(Command("get_article_audio"))
async def grammar_check(message: Message, state: FSMContext) -> None:
    await message.bot.send_message(chat_id=message.from_user.id, text="Сілтемені келесі хабарламамен жіберіңіз.\nБасқа ештеңе жібермеңіз. ")
    await state.set_state(MainState.get_audio_state)

@router.message(MainState.get_audio_state)
async def private_chat_summary_with_audio(message: Message, state: FSMContext) -> None:
    link = message.text
    title = bbc.get_title(link)
    text = bbc.get_article_text(link)
    image = bbc.get_image(link)
    general_prompt = """Summarize the following article. Ensure the summary captures the key points from the original 
    text without adding, removing, or interpreting any information. Use clear and concise language. Do not include 
    any personal opinions or assumptions."""

    if title:
        prompt = title + "\n" + text + "\n" + general_prompt
    else:
        prompt = text + "\n" + general_prompt
    try:
        response = test.post_request_kazllm(prompt)['vllm_response']['content']
        translation = test.translate_text(response)
        translation_text = translation['text']
        hex = test.get_audio(translation_text)
        base64 = base64_to_audio.hex_to_base64(hex)
        base64_to_audio.base64_to_audio(base64, "output.mp3")

        audio_path = "output.mp3"
        path = FSInputFile(audio_path)
        await message.bot.send_audio(chat_id=message.from_user.id, audio=path)
        print("Audio sent successfully!")
    except Exception as e:
        print(f"Failed to send message: {e}")
        await message.bot.send_message(chat_id=message.from_user.id, text="На данный момент, к сожалению, мы не можем обработать эту статью")
    try:
        caption = translation_text[:1024]
        remaining_text = translation_text[1024:]

        await message.bot.send_photo(chat_id=message.from_user.id, photo=image, caption=caption)

        if remaining_text:
            chunks = [remaining_text[i:i + 4096] for i in range(0, len(remaining_text), 4096)]
            for chunk in chunks:
                chunk = "Алдыңғы жазбаның жалғасы\n\n" + chunk
                await message.bot.send_message(chat_id=message.from_user.id, text=chunk)
    except Exception as e:
        print(f"Failed to send message: {e}")

    await state.clear()
