import asyncio
import hashlib
from youtube_search import YoutubeSearch
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

TOKEN = '6568437673:AAGrO83rdz0dMj3rO5S-7ymuPCPJjcmXTcc'
bot = Bot(token=TOKEN)
dp = Dispatcher()

def searcher(text):
    res = YoutubeSearch(text, max_results=5).to_dict()
    return res

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

@dp.inline_query()
async def inline_handler(query: types.InlineQuery):
    text = query.query or 'echo'
    links = searcher(text)

    articles = [
        types.InlineQueryResultArticle(
            id=hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
            title=f'{link["title"]}',
            url=f'https://www.youtube.com/watch?v={link["id"]}',
            thumbnail_url=f'{link["thumbnails"][0]}',
            input_message_content=types.InputTextMessageContent(
                message_text=f'https://www.youtube.com/watch?v={link["id"]}')
        ) for link in links]
    await query.answer(articles, cache_time=60, is_personal=True)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())