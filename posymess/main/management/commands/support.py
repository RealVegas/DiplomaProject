# Очистка списка команд (если он есть)
async def clear_commands(robot) -> None:
    current_commands = await robot.get_my_commands()
    if current_commands:
        await robot.set_my_commands([])