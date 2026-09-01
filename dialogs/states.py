from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()

class Select_collection_SG(StatesGroup):
    select_bricks = State()
    select_specific_brick_with_photo = State()
    select_kind_brick = State()
    select_layout_tile = State()

class Photo_visualization(StatesGroup):
    get_user_photo = State()
    processing_visualization = State()

class Forming_cards(StatesGroup):
    get_user_phone = State()
