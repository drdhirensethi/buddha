from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    visit_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    chief_complaint: Mapped[str | None] = mapped_column(String(255))
    history_of_present_illness: Mapped[str | None] = mapped_column(Text)
    assessment_summary: Mapped[str | None] = mapped_column(Text)
    plan: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="completed", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="visits")
    provider = relationship("User", back_populates="visits")

