import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.exceptions import TelegramNetworkError

from inits.logger import bot_logger


class OvayBot:
    def __init__(self, token, timeout=30, retry_attempts=3):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.timeout = timeout
        self.retry_attempts = retry_attempts

    async def start(self):
        bot = self.bot
        bot_logger.debug(f'Создан объект бота {bot}')
        dp = self.dp
        bot_logger.debug(f'Создан объект диспетчера {dp}')
        for attempt in range(self.retry_attempts):
            try:
                await bot.delete_webhook(drop_pending_updates=True)
                bot_logger.debug("Webhook deleted.")
                await bot.set_my_commands(
                    scope=types.BotCommandScopeAllPrivateChats()
                )
                await dp.start_polling(bot, timeout=self.timeout)
                bot_logger.debug('Запущен процесс polling')
                break
            except TelegramNetworkError as e:
                bot_logger.error(f"Ошибка сети: {e}.Повторная попытка... "
                                   f"(попытка {attempt + 1})")
                await asyncio.sleep(5)
            except Exception as e:
                bot_logger.error(f"Необработанная ошибка: {e}")
                await asyncio.sleep(5)
        else:
            bot_logger.error(f"Не удалось запустить бота после "
                             f"{self.retry_attempts} попыток.")

    def run(self):
        asyncio.run(self.start())
        bot_logger.debug('Запущен функция run бота на asyncio')

    async def info_message(self, chat_id, message):
        async with self.bot.session:
            try:
                await self.bot.send_message(chat_id, message)
                bot_logger.debug(f'Бот отправил сообщение {message }в чат{chat_id}')
            except Exception as e:
                bot_logger.error(f"Ошибка при отправке сообщения: {e}")

