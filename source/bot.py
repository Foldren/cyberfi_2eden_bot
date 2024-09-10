import logging
from asyncio import run
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandObject, Command
from aiogram.types import Message, MenuButtonWebApp, WebAppInfo
from tortoise import run_async, Tortoise
from tortoise.exceptions import IntegrityError
from components.tools import get_referral_reward
from config import TOKEN, WEB_APP_URL, TORTOISE_CONFIG
from db_models.api import User, Stats, Activity

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


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
        user = await User.create(id=message.from_user.id, country=language_code, rank_id=1)
        await Stats.create(id=user.id)
        await Activity.create(id=user.id)

        # Проверяем отправлен ли дополнительно реферальный код, если да то отправляем награду
        # https://t.me/twoeden_bot?start={referral_code}
        try:
            referral_code = command.args.split(" ")[0]
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
