from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager, StartMode
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.widgets.input import MessageInput

from dialogs import states
from config_data.config import load_config
from services.layouts import LAYOUTS


BRICK_TYPES = {
    'evro_type': 'Евро',
    'long_type': 'Лонг'
}


async def select_collection(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=states.Select_collection_SG.select_bricks)


async def material_selected(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, material_id: int):
    dialog_manager.dialog_data['material_id'] = material_id

    await dialog_manager.switch_to(states.Select_collection_SG.select_specific_brick_with_photo)


async def group_next(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    current_group = int(dialog_manager.dialog_data.get('group', 1))
    dialog_manager.dialog_data['group'] = min(current_group+1, 9)

    await dialog_manager.switch_to(states.Select_collection_SG.select_bricks)


async def group_prev(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    current_group = int(dialog_manager.dialog_data.get('group', 1))
    dialog_manager.dialog_data['group'] = max(current_group-1, 1)

    await dialog_manager.switch_to(states.Select_collection_SG.select_bricks)


async def brick_itog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=states.Select_collection_SG.select_kind_brick)


async def save_type_layout_itog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['type_layout'] = button.widget_id
    dialog_manager.dialog_data['layout_photo_path'] = LAYOUTS[button.widget_id]['photo']

    await dialog_manager.start(
        state=states.Photo_visualization.get_user_photo,
        data={
            'material_id': dialog_manager.dialog_data.get('material_id'),
            'brick_type': dialog_manager.dialog_data.get('brick_type'),
            'type_layout': dialog_manager.dialog_data.get('type_layout'),
            'layout_photo_path': dialog_manager.dialog_data.get('layout_photo_path')
        },
        mode=StartMode.RESET_STACK,
    )

async def back_to_choice_bricks(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=states.Select_collection_SG.select_bricks)


async def save_brick_type(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['brick_type'] = BRICK_TYPES[button.widget_id]

    await dialog_manager.switch_to(state=states.Select_collection_SG.select_layout_tile)



async def back_to_material_color(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=states.Select_collection_SG.select_bricks)


async def phone_received(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    i18n = dialog_manager.middleware_data['i18n']

    data = dialog_manager.start_data
    phone = message.contact.phone_number # type: ignore

    type_layout_none=dialog_manager.start_data.get('type_layout')

    type_layout=LAYOUTS[type_layout_none]['label']


    card = (
        f'{i18n.card.new()}\n'
        f'{i18n.card.material()}: {data.get("material_name")}\n' # type: ignore
        f'{i18n.card.brick.type()}: {data.get("brick_type")}\n' # type: ignore
        f'{i18n.card.phone()}: {phone}\n'
        f'{i18n.card.type.layout()}: {type_layout}\n'
        f'{i18n.card.result()}: {data.get("result_url")}' # type: ignore
    )

    for admin_id in load_config().tg_bot.superadmin:
        await message.bot.send_message(admin_id, card) # type: ignore

    await dialog_manager.done()
