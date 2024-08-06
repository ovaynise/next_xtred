from aiogram import types, Router

from inits.logger import bot_logger
from filters.chat_types import (
    ChatTypesFilter,
    UserLevelFilter,
    security_filters
)

group_and_private_router = Router()
common_filters = [
    ChatTypesFilter(['group', 'supergroup', 'channel', 'private']),
    UserLevelFilter(0, 15, "IsAuthUser")
]


@security_filters(
    group_and_private_router,
    'id',
    *common_filters
)
async def show_id(message: types.Message):
    bot_logger.debug('Отработала функция id')
    await message.answer(f'Ваш id: {message.from_user.id}, '
                         f'id чата: {message.chat.id}, '
                         f'id темы: {message.message_thread_id}')