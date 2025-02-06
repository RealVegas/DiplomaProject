# Очистка списка команд (если он есть)
async def clear_commands(robot) -> None:
    current_commands = await robot.get_my_commands()
    if current_commands:
        await robot.set_my_commands([])


# Получить пользователя
# def current_user(message: types.Message) -> User | None:
#     active_one = get_user()
#
#     if not active_one:
#         error_message = 'Вы не авторизованы, войдите в аккаунт на сайте'
#         message.answer(error_message)
#         return None
#     else:
#         return active_one