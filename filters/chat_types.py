from inits.logger import bot_logger
from utils.user_utils import get_user_level
from utils.security import crypt
from functools import wraps
from typing import Callable
from aiogram import Router, types
from aiogram.filters import Filter, Command


def log_filter_result(
        command: str,
        username: str,
        user_firstname: str,
        chat_title: str,
        chat_type: str,
        filter_name: str,
        result: bool,
        user_level: int = None):
    status = '🟡' if result else '🔴'
    user_info = (f'Пользователь @{username} ({user_firstname}) в чате '
                 f'{chat_title} ({chat_type}).')
    level_info = f' Уровень пользователя {user_level}.' \
        if user_level is not None else ''
    bot_logger.debug(
        f'{status}Команда "/{command}": Фильтр {filter_name}: '
        f'доступ {"разрешен" if result else "запрещен"}.\n'
        f'{user_info}{level_info}'
    )


def security_filters(router: Router, command: str, *filters: Filter):
    def decorator(handler: Callable):
        @wraps(handler)
        async def wrapper(message: types.Message):
            username = message.from_user.username or 'неизвестен'
            user_firstname = message.from_user.first_name
            chat_title = message.chat.title or f'личный чат ({message.chat.id})'
            user_id = message.from_user.id
            for filter_ in filters:
                if not await filter_(
                        message,
                        command,
                        username,
                        user_id,
                        user_firstname,
                        chat_title
                ):
                    return

            bot_logger.debug(
                f'🟢Команда "/{command}":\n'
                f'Все security_filters для {username} пройдены'
            )
            return await handler(message)

        router.message.register(wrapper, Command(command))
        return handler

    return decorator


class ChatTypesFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(
            self,
            message: types.Message,
            command: str,
            username: str,
            user_id: int,
            user_firstname: str,
            chat_title: str
    ) -> bool:
        result = message.chat.type in self.chat_types
        if not result:
            await message.answer(f'Команда /{command} доступна только в '
                                 f'следующих типах чатов: '
                                 f'{", ".join(self.chat_types)}.')
        log_filter_result(
            command,
            username,
            user_firstname,
            chat_title,
            message.chat.type,
            'ChatTypesFilter', result
        )
        return result


class UserLevelFilter(Filter):
    def __init__(
            self,
            min_level: int,
            max_level: int,
            filter_name: str
    ) -> None:
        self.min_level = min_level
        self.max_level = max_level
        self.filter_name = filter_name

    async def __call__(
            self,
            message: types.Message,
            command: str, username: str,
            user_id: int, user_firstname: str,
            chat_title: str
    ) -> bool:
        user_level = await get_user_level(crypt(user_id))
        result = (user_level
                  is not None and
                  self.min_level <= user_level <= self.max_level)
        if not result:
            if user_level is None:
                await message.answer(f'Для выполнения команды /{command} '
                                     f'необходимо зарегистрироваться. '
                                     f'Введите /start для регистрации.')
            else:
                await message.answer(f'Для выполнения команды /{command} '
                                     f'необходим уровень доступа '
                                     f'от {self.min_level} до {self.max_level}'
                                     f'. Ваш уровень: {user_level}.')
        log_filter_result(
            command,
            username,
            user_firstname,
            chat_title,
            message.chat.type,
            self.filter_name,
            result,
            user_level
        )
        return result


class IsAnonymousUser(Filter):
    async def __call__(
            self,
            message: types.Message,
            command: str, username: str,
            user_id: int,
            user_firstname: str,
            chat_title: str) -> bool:
        if message.from_user.is_bot or message.from_user.id is None:
            bot_logger.debug(
                f'🟡Команда "/{command}": Фильтр '
                f'IsAnonymousUser: пользователь анонимен или бот.\n'
                f'Пользователь @{username} ({user_firstname}) в '
                f'чате {chat_title}.'
            )
            await message.answer(f'Команда /{command} не доступна для '
                                 f'анонимных пользователей или ботов.')
            return False
        return True


group_and_private_router = Router()
common_filters = [
    ChatTypesFilter(['group', 'supergroup', 'channel', 'private']),
    IsAnonymousUser(),
    UserLevelFilter(0, 15, 'IsAuthUser')
]


@security_filters(
    group_and_private_router,
    'id',
    *common_filters)
async def show_id(message: types.Message):
    bot_logger.debug('Отработала функция id')
    await message.answer(f'Ваш id: {message.from_user.id}, '
                         f'id чата: {message.chat.id}, '
                         f'id темы: {message.message_thread_id}')
