from datetime import datetime


# Очистка списка команд (если он есть)
async def clear_commands(robot) -> None:
    current_commands = await robot.get_my_commands()
    if current_commands:
        await robot.set_my_commands([])


# Создание списка заказов в виде списка словарей
def orders_list(orders) -> list[dict[str, str | float]]:
    new_orders: list[dict[str, str | float]] = []

    for one_item in orders:
        temp_dict: dict[str, str | float] = {
            'id': one_item.id,
            'posy_name': one_item.flower.posy_name,
            'order_date': datetime.strftime(one_item.order_date, format='%d.%m.%Y'),
            'order_price': float(one_item.order_price)
        }

        new_orders.append(temp_dict)

    return new_orders


# Создание списка букетов в виде списка словарей
def posy_list(flowers) -> list[dict[str, str | float]]:
    new_posies: list[dict[str, str | float]] = []

    for one_item in flowers:
        temp_dict: dict[str, str | float] = {
            'id': one_item.id,
            'posy_name': one_item.posy_name,
            'price': float(one_item.price),
            'posy_path': one_item.posy_path,
            'telegram_id': one_item.telegram_id
        }

        new_posies.append(temp_dict)

    return new_posies