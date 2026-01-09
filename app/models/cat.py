from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class SpyCat(Base):
    __tablename__ = "cats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    years_of_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    breed: Mapped[str] = mapped_column(String(100), nullable=False)
    salary: Mapped[int] = mapped_column(Integer, nullable=False)

    mission: Mapped["Mission"] = relationship(
        back_populates="cat",
        uselist=False,
    )
