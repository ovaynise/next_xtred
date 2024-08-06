from aiogram import Router, types

from filters.chat_types import (
    ChatTypesFilter,
    UserLevelFilter,
    security_filters
)


super_user_router = Router()
common_filters = [
    ChatTypesFilter(['group', 'supergroup', 'channel', 'private']),
    UserLevelFilter(0, 0, "IsSuperUser")
]


@security_filters(
    super_user_router,
    'su',
    *common_filters
)
async def su_test(message: types.Message):
    await message.answer(f'SUPERUSER, подтвержен: '
                         f'{message.from_user.username}')