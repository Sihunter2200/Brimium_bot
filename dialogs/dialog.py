from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select, Row, Column, RequestContact
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram.enums import ContentType

from dialogs import getters, states
from dialogs import callbacks
from services import dialog_widgets
from services.layouts import LAYOUTS


start_dialog = Dialog(
    Window(Format('{start_bot}'),
            DynamicMedia('photo'),
            Button(Format('{button_start}'), id='button_start', on_click=callbacks.select_collection),
        getter=getters.start_hi,
        state=states.StartSG.start)
    )


select_collection = Dialog(
    Window(
        Format('{collection_select}'),
        DynamicMedia('photo'),
        ScrollingGroup(
            Select(
                Format('{item[name]}'),
                id='collect',
                item_id_getter=lambda item: item['id'],
                items='materials',
                on_click=callbacks.material_selected # type: ignore
            ),
            id='material_scroll',
            width=1,
            height=7,
            hide_on_single_page=True
        ),
        Row(
            Button(Const('←'), id='group_prev', on_click=callbacks.group_prev),
            Button(Const('→'), id='group_next', on_click=callbacks.group_next)
        ),
        state=states.Select_collection_SG.select_bricks,
        getter=getters.material_selection),
    Window(
        DynamicMedia('photo'),
        Column(
            Button(Format('{choice_brick_itog}'), id='choice_brick_itog', on_click=callbacks.brick_itog),
            Button(Format('{choice_brick_back}'), id='choice_brick_back', on_click=callbacks.back_to_choice_bricks)
            ),
        state=states.Select_collection_SG.select_specific_brick_with_photo,
        getter=getters.select_photo_by_brick_type
    ),
    Window(
        Format('{choice_kind_brick}'),
        Column(
            Button(Format('{evro_type}'), id='evro_type', on_click=callbacks.save_brick_type),
            Button(Format('{long_type}'), id='long_type', on_click=callbacks.save_brick_type),
        ),
        state=states.Select_collection_SG.select_kind_brick,
        getter=getters.kind_brick_gett
    ),
    Window(
        DynamicMedia('photo'),
        Format('{choice_layout_tile}'),
        Column(
            Button(Const(LAYOUTS['horizontal_straight']['label']), id='horizontal_straight', on_click=callbacks.save_type_layout_itog),
            Button(Const(LAYOUTS['horizontal_staggered']['label']), id='horizontal_staggered', on_click=callbacks.save_type_layout_itog),
            Button(Const(LAYOUTS['vertical_straight']['label']), id='vertical_straight', on_click=callbacks.save_type_layout_itog),
            Button(Const(LAYOUTS['vertical_staggered']['label']), id='vertical_staggered', on_click=callbacks.save_type_layout_itog)
        ),
        state=states.Select_collection_SG.select_layout_tile,
        getter=getters.layout_tile_gett
    ),
)


get_photo_user = Dialog(
    Window(
        Format('{waiting_photo}'),
        MessageInput(
            func=dialog_widgets.save_photo,
            content_types=ContentType.PHOTO
        ),
        state=states.Photo_visualization.get_user_photo,
        getter=getters.photo_reception
    ),

    Window(
        Format('{process_visual}'),
        state=states.Photo_visualization.processing_visualization,
        getter=getters.photo_in_process
    ),
)


forming_cards = Dialog(
    Window(
        Format('{ask_phone}'),
        RequestContact(Format('{share_phone}')),
        MessageInput(
            func=callbacks.phone_received,
            content_types=ContentType.CONTACT

        ),
        state=states.Forming_cards.get_user_phone,
        getter=getters.user_phone,
        markup_factory=ReplyKeyboardFactory(resize_keyboard=True)
    )
)