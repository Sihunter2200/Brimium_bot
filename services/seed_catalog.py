import asyncio

from sqlalchemy.dialects.postgresql import insert as pg_insert

from database.db import async_session
from database.models import Material

IMAGES_DIR = 'data/images'

# group -> путь к общему фото группы
GROUP_PHOTOS = {
    1: 'data/images/menu_group_1.jpg',
    2: 'data/images/menu_group_2.jpg',
    3: 'data/images/menu_group_3.jpg',
    4: 'data/images/menu_group_4.jpg',
    5: 'data/images/menu_group_5.jpg',
    6: 'data/images/menu_group_6.jpg',
    7: 'data/images/menu_group_7.jpg',
    8: 'data/images/menu_group_8.jpg',
    9: 'data/images/menu_group_9.jpg',
}

# (имя, группа, имя файла) — порядок задаёт порядок показа в меню.
# имя файла в data/images: {имя}_{номер}.jpg
MATERIALS = [
    ('T-32', 1, 'T-32_1.jpg'),
    ('T-53', 1, 'T-53_2.jpg'),
    ('T-62', 1, 'T-62_3.jpg'),
    ('T-75', 1, 'T-75_4.jpg'),
    ('T-19', 1, 'T-19_5.jpg'),
    ('T-55', 1, 'T-55_6.jpg'),
    ('T-04', 1, 'T-04_7.jpg'),

    ('T-26', 2, 'T-26_8.jpg'),
    ('T-37', 2, 'T-37_9.jpg'),
    ('T-96.22', 2, 'T-96.22_10.jpg'),
    ('T-51', 2, 'T-51_11.jpg'),
    ('T-99', 2, 'T-99_12.jpg'),
    ('T-79', 2, 'T-79_13.jpg'),
    ('T-92', 2, 'T-92_14.jpg'),

    ('T-15', 3, 'T-15_15.jpg'),
    ('T-92.2', 3, 'T-92.2_16.jpg'),
    ('T-91', 3, 'T-91_17.jpg'),
    ('T-91.1', 3, 'T-91.1_18.jpg'),
    ('T-91.2', 3, 'T-91.2_19.jpg'),
    ('T-07 (1)', 3, 'T-07_20(1).jpg'),
    ('T-71', 3, 'T-71_21.jpg'),

    ('T-16', 4, 'T-16_22.jpg'),
    ('T-12', 4, 'T-12_23.jpg'),
    ('T-59', 4, 'T-59_24.jpg'),
    ('T-22', 4, 'T-22_25.jpg'),
    ('T-11', 4, 'T-11_26.jpg'),
    ('T-54', 4, 'T-54_27.jpg'),
    ('T-41', 4, 'T-41_28.jpg'),

    ('T-99.2', 5, 'T-99.2_29.jpg'),
    ('S-17', 5, 'S-17_30.jpg'),
    ('T-30', 5, 'T-30_31.jpg'),
    ('T-56 NEW', 5, 'T-56 NEW_32.jpg'),
    ('T-77', 5, 'T-77_33.jpg'),
    ('T-81', 5, 'T-81_34.jpg'),
    ('T-56.1', 5, 'T-56.1_35.jpg'),

    ('T-60', 6, 'T-60_36.jpg'),
    ('T-90', 6, 'T-90_37.jpg'),
    ('T-56 OLD', 6, 'T-56 OLD_38.jpg'),
    ('T-59.2', 6, 'T-59.2_39.jpg'),
    ('T-90.1', 6, 'T-90.1_40.jpg'),
    ('K-55', 6, 'K-55_41.jpg'),
    ('K-92', 6, 'K-92_42.jpg'),

    ('T-15.1', 7, 'T-15.1_43.jpg'),
    ('T-50', 7, 'T-50_44.jpg'),
    ('T-11.1', 7, 'T-11.1_45.jpg'),
    ('T-07 (2)', 7, 'T-07_46(2).jpg'),
    ('T-20', 7, 'T-20_47.jpg'),
    ('T-76', 7, 'T-76_48.jpg'),
    ('T-04.1', 7, 'T-04.1_49.jpg'),

    ('T-04.2', 8, 'T-04.2_50.jpg'),
    ('T-38', 8, 'T-38_51.jpg'),
    ('T-53.1', 8, 'T-53.1_52.jpg'),
    ('T-04.3', 8, 'T-04.3_53.jpg'),
    ('T-105', 8, 'T-105_54.jpg'),
    ('T-103', 8, 'T-103_55.jpg'),
    ('T-103.1', 8, 'T-103.1_56.jpg'),

    ('T-104', 9, 'T-104_57.jpg'),
    ('T-107', 9, 'T-107_58.jpg'),
    ('T-106', 9, 'T-106_59.jpg'),
    ('T-55.1', 9, 'T-55.1_60.jpg'),
    ('TT-01', 9, 'TT-01_61.jpg'),
    ('T(1)', 9, 'T(1)_62.jpg'),
    ('T(2)', 9, 'T(2)_63.jpg'),
]


async def seed_catalog():
    async with async_session() as session:
        for name, group, filename in MATERIALS:
            brick_photo_path = f'{IMAGES_DIR}/{filename}'
            ins = pg_insert(Material)
            stmt = (
                ins
                .values(
                    name=name,
                    group=group,
                    menu_photo_path=GROUP_PHOTOS[group],
                    brick_photo_path=brick_photo_path,
                )
                .on_conflict_do_update(
                    index_elements=[Material.name],
                    set_={
                        'group': ins.excluded.group,
                        'menu_photo_path': ins.excluded.menu_photo_path,
                        'brick_photo_path': ins.excluded.brick_photo_path,
                    },
                )
            )
            await session.execute(stmt)

        await session.commit()
    print(f'Загружено материалов: {len(MATERIALS)}')


if __name__ == '__main__':
    asyncio.run(seed_catalog())
