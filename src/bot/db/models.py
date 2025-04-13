from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.bot.db.schemas import DataFromTablesSchema


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DataFromTablesModel(Base):
    __tablename__ = "data_from_tables"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=True, default='')
    url: Mapped[str] = mapped_column(nullable=True, default='')
    xpath: Mapped[str] = mapped_column(nullable=True, default='')

    def to_read_model(self) -> DataFromTablesSchema:
        return DataFromTablesSchema(
            title=self.title,
            url=self.url,
            xpath=self.xpath,
        )
