import asyncio  # noqa

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
    Не буду делать избыточный унифицированный сервис через зависимости, репозитории. KISS
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
            error_logger(f'Не получилось добавить запись в таблицу: {model_schema}\n'
                         f'Ошибка {repr(e)}')

# asyncio.run(create_tables())
