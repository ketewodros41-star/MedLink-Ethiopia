"""initial schema

Revision ID: 20260510_0001
Revises:
Create Date: 2026-05-10 18:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260510_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "pharmacies",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("region", sa.String(length=120), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("contact_phone", sa.String(length=32), nullable=True),
        sa.Column("verified_pharmacist", sa.Boolean(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("response_speed_score", sa.Float(), nullable=False),
        sa.Column("stock_reliability_score", sa.Float(), nullable=False),
        sa.Column("fulfillment_score", sa.Float(), nullable=False),
        sa.Column("counterfeit_risk_score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("contact_phone"),
    )
    op.create_index(op.f("ix_pharmacies_name"), "pharmacies", ["name"], unique=False)

    op.create_table(
        "medicines",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("canonical_name", sa.String(length=255), nullable=False),
        sa.Column("generic_name", sa.String(length=255), nullable=False),
        sa.Column("strength", sa.String(length=64), nullable=True),
        sa.Column("form", sa.String(length=64), nullable=True),
        sa.Column("therapeutic_class", sa.String(length=120), nullable=True),
        sa.Column("search_vector", sa.String(length=255), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("canonical_name"),
    )
    op.create_index(op.f("ix_medicines_generic_name"), "medicines", ["generic_name"], unique=False)
    op.create_index(op.f("ix_medicines_search_vector"), "medicines", ["search_vector"], unique=False)

    op.create_table(
        "medicine_aliases",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("medicine_id", sa.String(length=36), nullable=False),
        sa.Column("alias", sa.String(length=255), nullable=False),
        sa.Column("normalized_alias", sa.String(length=255), nullable=False),
        sa.Column("locale", sa.String(length=16), nullable=False),
        sa.Column("alias_type", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["medicine_id"], ["medicines.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_medicine_aliases_alias"), "medicine_aliases", ["alias"], unique=False)
    op.create_index(op.f("ix_medicine_aliases_medicine_id"), "medicine_aliases", ["medicine_id"], unique=False)
    op.create_index(op.f("ix_medicine_aliases_normalized_alias"), "medicine_aliases", ["normalized_alias"], unique=False)

    op.create_table(
        "inventory_items",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("pharmacy_id", sa.String(length=36), nullable=False),
        sa.Column("medicine_id", sa.String(length=36), nullable=False),
        sa.Column("quantity_available", sa.Integer(), nullable=False),
        sa.Column("quantity_reserved", sa.Integer(), nullable=False),
        sa.Column("verification_count", sa.Integer(), nullable=False),
        sa.Column("last_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_verified_by", sa.String(length=120), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("state", sa.String(length=32), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["medicine_id"], ["medicines.id"]),
        sa.ForeignKeyConstraint(["pharmacy_id"], ["pharmacies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_inventory_items_medicine_id"), "inventory_items", ["medicine_id"], unique=False)
    op.create_index(op.f("ix_inventory_items_pharmacy_id"), "inventory_items", ["pharmacy_id"], unique=False)

    op.create_table(
        "reservations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=120), nullable=False),
        sa.Column("pharmacy_id", sa.String(length=36), nullable=False),
        sa.Column("medicine_id", sa.String(length=36), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("approval_required", sa.Boolean(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["medicine_id"], ["medicines.id"]),
        sa.ForeignKeyConstraint(["pharmacy_id"], ["pharmacies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reservations_medicine_id"), "reservations", ["medicine_id"], unique=False)
    op.create_index(op.f("ix_reservations_pharmacy_id"), "reservations", ["pharmacy_id"], unique=False)
    op.create_index(op.f("ix_reservations_user_id"), "reservations", ["user_id"], unique=False)

    op.create_table(
        "community_stock_reports",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=120), nullable=False),
        sa.Column("medicine_id", sa.String(length=36), nullable=False),
        sa.Column("pharmacy_id", sa.String(length=36), nullable=False),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.Column("photo_proof_url", sa.String(length=512), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("reputation_weight", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["medicine_id"], ["medicines.id"]),
        sa.ForeignKeyConstraint(["pharmacy_id"], ["pharmacies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_community_stock_reports_medicine_id"), "community_stock_reports", ["medicine_id"], unique=False)
    op.create_index(op.f("ix_community_stock_reports_pharmacy_id"), "community_stock_reports", ["pharmacy_id"], unique=False)
    op.create_index(op.f("ix_community_stock_reports_user_id"), "community_stock_reports", ["user_id"], unique=False)

    op.create_table(
        "sync_operations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.String(length=120), nullable=False),
        sa.Column("user_id", sa.String(length=120), nullable=False),
        sa.Column("operation_type", sa.String(length=64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("conflict_reason", sa.String(length=255), nullable=True),
        sa.Column("received_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sync_operations_client_id"), "sync_operations", ["client_id"], unique=False)
    op.create_index(op.f("ix_sync_operations_user_id"), "sync_operations", ["user_id"], unique=False)

    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("event_type", sa.String(length=120), nullable=False),
        sa.Column("actor_id", sa.String(length=120), nullable=False),
        sa.Column("aggregate_type", sa.String(length=120), nullable=False),
        sa.Column("aggregate_id", sa.String(length=120), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_events_actor_id"), "audit_events", ["actor_id"], unique=False)
    op.create_index(op.f("ix_audit_events_aggregate_id"), "audit_events", ["aggregate_id"], unique=False)
    op.create_index(op.f("ix_audit_events_created_at"), "audit_events", ["created_at"], unique=False)
    op.create_index(op.f("ix_audit_events_event_type"), "audit_events", ["event_type"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_audit_events_event_type"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_created_at"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_aggregate_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_actor_id"), table_name="audit_events")
    op.drop_table("audit_events")
    op.drop_index(op.f("ix_sync_operations_user_id"), table_name="sync_operations")
    op.drop_index(op.f("ix_sync_operations_client_id"), table_name="sync_operations")
    op.drop_table("sync_operations")
    op.drop_index(op.f("ix_community_stock_reports_user_id"), table_name="community_stock_reports")
    op.drop_index(op.f("ix_community_stock_reports_pharmacy_id"), table_name="community_stock_reports")
    op.drop_index(op.f("ix_community_stock_reports_medicine_id"), table_name="community_stock_reports")
    op.drop_table("community_stock_reports")
    op.drop_index(op.f("ix_reservations_user_id"), table_name="reservations")
    op.drop_index(op.f("ix_reservations_pharmacy_id"), table_name="reservations")
    op.drop_index(op.f("ix_reservations_medicine_id"), table_name="reservations")
    op.drop_table("reservations")
    op.drop_index(op.f("ix_inventory_items_pharmacy_id"), table_name="inventory_items")
    op.drop_index(op.f("ix_inventory_items_medicine_id"), table_name="inventory_items")
    op.drop_table("inventory_items")
    op.drop_index(op.f("ix_medicine_aliases_normalized_alias"), table_name="medicine_aliases")
    op.drop_index(op.f("ix_medicine_aliases_medicine_id"), table_name="medicine_aliases")
    op.drop_index(op.f("ix_medicine_aliases_alias"), table_name="medicine_aliases")
    op.drop_table("medicine_aliases")
    op.drop_index(op.f("ix_medicines_search_vector"), table_name="medicines")
    op.drop_index(op.f("ix_medicines_generic_name"), table_name="medicines")
    op.drop_table("medicines")
    op.drop_index(op.f("ix_pharmacies_name"), table_name="pharmacies")
    op.drop_table("pharmacies")
