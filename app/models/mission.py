from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    cat_id: Mapped[int | None] = mapped_column(
        ForeignKey("cats.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )

    cat: Mapped["SpyCat"] = relationship(back_populates="mission")
    targets: Mapped[list["Target"]] = relationship(
        back_populates="mission",
        cascade="all, delete-orphan",
    )
