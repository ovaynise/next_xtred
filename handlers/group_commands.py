from aiogram import Router


from filters.chat_types import (
    ChatTypesFilter,
    UserLevelFilter,
    security_filters
)


group_commands_router = Router()
common_filters = [
    ChatTypesFilter(['group', 'supergroup', 'channel']),
    UserLevelFilter(0, 15, "IsAuthUser")
]








