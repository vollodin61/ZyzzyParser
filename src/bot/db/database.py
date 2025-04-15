import asyncio  # noqa

import pandas as pd
from sqlalchemy import insert

from src.bot.db.db_config import DBConfig
from src.bot.db.models import Base, DataFromTablesModel
from src.bot.db.schemas import DataFromTablesSchema
from src.bot.utils.decorators import safe_call_dec
from src.config import info_logger, error_logger


async def create_tables():
    async with DBConfig.async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@safe_call_dec
async def add_line_to_db(model_schema: DataFromTablesSchema):
    """
    Это простой способ добавлять в базу записи. Достаточно для маленьких проектов
    :param model_schema:
    :return:
    """
    async with DBConfig.async_session_factory() as session:
        session.add(DataFromTablesModel(**model_schema.model_dump(exclude_unset=True)))
        await session.commit()
        info_logger(f'В базу добавлена запись {model_schema}')


async def add_line_to_data_from_tables(model_schema: DataFromTablesSchema):
    """
    Продвинутый способ. Уже возвращаем id, если понадобится дальнейшее взаимодействие.
    Но работает только с конкретной моделью. Достаточно для маленьких проектов.
    Не буду делать избыточный унифицированный сервис с зависимостями, абстрактными классами,
    собственным контекстным менеджером, который прокидывает и управляет сессией. KISS
    :param model_schema:
    :return: id добавленной записи
    """
    async with DBConfig.async_session_factory() as session:
        try:
            stmt = (insert(DataFromTablesModel)
                    .values(**model_schema.model_dump(exclude_unset=True))
                    .returning(DataFromTablesModel.id))
            res = await session.execute(stmt)
            await session.commit()
            info_logger(f'В базу добавлена запись {model_schema}')
            return res.scalar_one_or_none()
        except Exception as e:
            await session.rollback()
            error_logger(f'Не получилось добавить запись в таблицу: {model_schema}\n'
                         f'Ошибка {repr(e)}')


async def save_data_from_tables_to_db(file_path, chunk_size: int = 100):
    """
    Сохраняем данные из таблицы в базу, будем пачками запихивать

    :param file_path: путь к файлу, который прислал пользователь и мы его уже проверили на валидность и сохранили
    :param chunk_size: размер пакета для вставки в бд
    :return:
    """
    df = pd.read_excel(file_path)

    #  Вначале преобразуем
    try:
        records = [
            DataFromTablesSchema(
                title=row['title'],
                url=row['url'],
                xpath=row['xpath']
            )
            for _, row in df.iterrows()
        ]
    except Exception as e:
        error_logger(f'Ошибка преобразования данных: {repr(e)}')

    success = 0
    errors = 0

    async with DBConfig.async_session_factory() as session:
        for i in range(0, len(records), chunk_size):
            chunk = records[i:i + chunk_size]

            try:
                chunk_dicts = [item.model_dump() for item in chunk]

                await session.execute(
                    insert(DataFromTablesModel), chunk_dicts
                )
                await session.commit()
                success += len(chunk)
            except Exception as e:
                await session.rollback()
                errors += len(chunk)
                error_logger(f"Ошибка при вставке данных в базу: {repr(e)}")
                continue
    info_logger(f'\nУспешно добавлено: {success}\n'
                f'Ошибок при добавлении: {errors}')

# asyncio.run(create_tables())
