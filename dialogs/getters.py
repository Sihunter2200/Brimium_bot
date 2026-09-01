from aiogram_dialog import DialogManager
from aiogram.types import User
from aiogram import html
from fluentogram import TranslatorRunner
from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment

from database.db import async_session
from database import requests

async def start_hi(dialog_manager: DialogManager,
                    i18n: TranslatorRunner,
                    **kwargs):
    photo = MediaAttachment(type=ContentType.PHOTO, path='data/images/brimium_start_photo.jpg')

    return {'start_bot': i18n.start.bot(),
            'button_start': i18n.button.start(),
            'photo': photo}


async def material_selection(dialog_manager: DialogManager,
                            i18n: TranslatorRunner,
                            **kwargs):
    group = int(dialog_manager.dialog_data.get('group', 1))

    async with async_session() as session:
        materials = await requests.get_material_by_group(session, group)
        menu_photo = await requests.get_photo_by_group(session, group)

    photo = MediaAttachment(
		type=ContentType.PHOTO,
		path=menu_photo or 'data/images/brimium_start_photo.jpg'
	)

    return {'materials': [{'id': m.id, 'name': m.name} for m in materials],
            'photo': photo,
            'collection_select': i18n.collection.select()}

async def layout_tile_gett(dialog_manager: DialogManager,
                                i18n: TranslatorRunner,
                                **kwargs):
    photo = MediaAttachment(type=ContentType.PHOTO, path='data/images/menu_layout_photo.jpg')

    return {'choice_layout_tile': i18n.choice.layout.tile(),
            'photo': photo}


async def select_photo_by_brick_type(dialog_manager: DialogManager,
                                i18n: TranslatorRunner,
                                **kwargs):
    material_id = int(dialog_manager.dialog_data.get('material_id')) # type: ignore

    async with async_session() as session:
        path = await requests.get_photo_by_material_id(session, material_id)

    photo = MediaAttachment(
        type=ContentType.PHOTO,
        path=path if path else None
    )

    return {'photo': photo,
            'choice_brick_itog': i18n.choice.brick.itog(),
            'choice_brick_back': i18n.choice.brick.back()}


async def kind_brick_gett(dialog_manager: DialogManager,
                        i18n: TranslatorRunner,
                        **kwargs):
    return {'choice_kind_brick': i18n.choice.kind.brick(),
            'evro_type': i18n.evro.type(),
            'long_type': i18n.long.type()}


async def photo_reception(dialog_manager: DialogManager,
                            i18n: TranslatorRunner,
                            **kwargs):

    return {'waiting_photo': i18n.waiting.photo()}


async def photo_in_process(dialog_manager: DialogManager,
                            i18n: TranslatorRunner,
                            **kwargs):
    return {'process_visual': i18n.process.visual()}


async def user_phone(dialog_manager: DialogManager,
                        i18n: TranslatorRunner,
                        **kwargs):

    return {'ask_phone': i18n.ask.phone(),
            'share_phone': i18n.share.phone()}