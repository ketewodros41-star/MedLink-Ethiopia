from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import uuid4

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def new_id() -> str:
    return str(uuid4())


class UserRole(StrEnum):
    PATIENT = "patient"
    PHARMACIST = "pharmacist"
    ADMIN = "admin"


class InventoryState(StrEnum):
    UNVERIFIED = "unverified"
    ESTIMATED = "estimated"
    RECENTLY_VERIFIED = "recently_verified"
    STALE = "stale"
    UNAVAILABLE = "unavailable"


class ReservationStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    FULFILLED = "fulfilled"


class SyncStatus(StrEnum):
    QUEUED = "queued"
    APPLIED = "applied"
    REJECTED = "rejected"


class Pharmacy(Base):
    __tablename__ = "pharmacies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    city: Mapped[str] = mapped_column(String(120), nullable=False, default="Addis Ababa")
    region: Mapped[str] = mapped_column(String(120), nullable=False, default="Addis Ababa")
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    contact_phone: Mapped[str | None] = mapped_column(String(32), unique=True)
    verified_pharmacist: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    response_speed_score: Mapped[float] = mapped_column(Float, default=0.7)
    stock_reliability_score: Mapped[float] = mapped_column(Float, default=0.7)
    fulfillment_score: Mapped[float] = mapped_column(Float, default=0.7)
    counterfeit_risk_score: Mapped[float] = mapped_column(Float, default=0.05)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class Medicine(Base):
    __tablename__ = "medicines"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    canonical_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    generic_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    strength: Mapped[str | None] = mapped_column(String(64))
    form: Mapped[str | None] = mapped_column(String(64))
    therapeutic_class: Mapped[str | None] = mapped_column(String(120))
    search_vector: Mapped[str] = mapped_column(String(255), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    aliases: Mapped[list["MedicineAlias"]] = relationship(back_populates="medicine", cascade="all, delete-orphan")


class MedicineAlias(Base):
    __tablename__ = "medicine_aliases"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    medicine_id: Mapped[str] = mapped_column(ForeignKey("medicines.id", ondelete="CASCADE"), index=True)
    alias: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    normalized_alias: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    locale: Mapped[str] = mapped_column(String(16), default="en")
    alias_type: Mapped[str] = mapped_column(String(32), default="synonym")

    medicine: Mapped["Medicine"] = relationship(back_populates="aliases")


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    pharmacy_id: Mapped[str] = mapped_column(ForeignKey("pharmacies.id"), index=True)
    medicine_id: Mapped[str] = mapped_column(ForeignKey("medicines.id"), index=True)
    quantity_available: Mapped[int] = mapped_column(Integer, default=0)
    quantity_reserved: Mapped[int] = mapped_column(Integer, default=0)
    verification_count: Mapped[int] = mapped_column(Integer, default=0)
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_verified_by: Mapped[str | None] = mapped_column(String(120))
    confidence_score: Mapped[float] = mapped_column(Float, default=0.25)
    state: Mapped[str] = mapped_column(String(32), default=InventoryState.UNVERIFIED.value)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    user_id: Mapped[str] = mapped_column(String(120), index=True)
    pharmacy_id: Mapped[str] = mapped_column(ForeignKey("pharmacies.id"), index=True)
    medicine_id: Mapped[str] = mapped_column(ForeignKey("medicines.id"), index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default=ReservationStatus.PENDING.value)
    approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class CommunityStockReport(Base):
    __tablename__ = "community_stock_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    user_id: Mapped[str] = mapped_column(String(120), index=True)
    medicine_id: Mapped[str] = mapped_column(ForeignKey("medicines.id"), index=True)
    pharmacy_id: Mapped[str] = mapped_column(ForeignKey("pharmacies.id"), index=True)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False)
    photo_proof_url: Mapped[str | None] = mapped_column(String(512))
    notes: Mapped[str | None] = mapped_column(Text)
    reputation_weight: Mapped[float] = mapped_column(Float, default=0.5)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SyncOperation(Base):
    __tablename__ = "sync_operations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    client_id: Mapped[str] = mapped_column(String(120), index=True)
    user_id: Mapped[str] = mapped_column(String(120), index=True)
    operation_type: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(32), default=SyncStatus.QUEUED.value)
    conflict_reason: Mapped[str | None] = mapped_column(String(255))
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    event_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    actor_id: Mapped[str] = mapped_column(String(120), index=True)
    aggregate_type: Mapped[str] = mapped_column(String(120), nullable=False)
    aggregate_id: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
