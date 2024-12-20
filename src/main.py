import logging
from asyncio import run
from io import BytesIO
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandObject, Command
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, MenuButtonWebApp, WebAppInfo
from redis.asyncio import Redis
from tortoise import run_async, Tortoise
from tortoise.exceptions import IntegrityError
from components.tools import get_referral_reward
from config import TOKEN, WEB_APP_URL, TORTOISE_CONFIG, REDIS_URL
from models import User, Stats, Activity

# Используемые базы данных Redis
# db 0 - кеш для стейтов бота
# db9 - Для asgi_limit
# db10 - Кеш fastapi_cache

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=RedisStorage(Redis.from_url(REDIS_URL, db=0)), key_builder=DefaultKeyBuilder(with_destiny=True))


async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=["message", "callback_query"])

    # Добавим кнопку меню с игрой
    await bot.set_chat_menu_button(menu_button=MenuButtonWebApp(text="Игра", web_app=WebAppInfo(url=WEB_APP_URL)))


@dp.message(Command("start"))
async def start(message: Message, command: CommandObject):
    # Добавим кнопку меню с игрой
    await bot.set_chat_menu_button(
        chat_id=message.from_user.id,
        menu_button=MenuButtonWebApp(text="Игра", web_app=WebAppInfo(url=WEB_APP_URL))
    )

    # Пытаемся создать пользователя, если его нет
    try:
        language_code = message.from_user.language_code.upper()
        user_avatars = await bot.get_user_profile_photos(user_id=message.from_user.id)
        io = BytesIO()

        if user_avatars.total_count != 0:
            await bot.download(file=user_avatars.photos[0][0].file_id, destination=io)
            avatar_bytes = io.getvalue()
        else:
            avatar_bytes = None

        user = await User.create(id=message.from_user.id,
                                 country=language_code,
                                 username=message.from_user.username,
                                 avatar=avatar_bytes)

        await Stats.create(user_id=user.id)
        await Activity.create(user_id=user.id)

        # Проверяем отправлен ли дополнительно реферальный код, если да то отправляем награду
        try:
            referral_code = command.args.strip()
            await get_referral_reward(user, referral_code)
        except AttributeError:
            pass

    except IntegrityError:
        pass

    await message.answer(text="Привет, я бот тест для WebApp\n"
                              "нажми на кнопку <b>Игра</b> чтобы начать 😉")


if __name__ == "__main__":
    run_async(Tortoise.init(TORTOISE_CONFIG))
    run(main())
