"""initial schema

Revision ID: 20260205_0001
Revises:
Create Date: 2026-02-05
"""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260205_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # cities
    op.create_table(
        "cities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("country", sa.String(length=255), nullable=True),
        sa.Column("state", sa.String(length=255), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
    )

    # areas
    op.create_table(
        "areas",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "city_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("cities.id", onupdate="CASCADE", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("postal_code", sa.String(length=20), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
    )

    # vendors
    op.create_table(
        "vendors",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column(
            "city_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("cities.id", onupdate="CASCADE", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "area_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("areas.id", onupdate="CASCADE", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
    )

    # vendor_types
    op.create_table(
        "vendor_types",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("code", name="uq_vendor_types_code"),
    )

    # materials
    op.create_table(
        "materials",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("code", name="uq_materials_code"),
    )

    # brands
    op.create_table(
        "brands",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("code", name="uq_brands_code"),
    )

    # target_groups
    op.create_table(
        "target_groups",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("code", name="uq_target_groups_code"),
    )

    # junction tables
    op.create_table(
        "vendor_vendor_types",
        sa.Column(
            "vendor_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("vendors.id", onupdate="CASCADE", ondelete="RESTRICT"),
            primary_key=True,
        ),
        sa.Column(
            "vendor_type_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("vendor_types.id", onupdate="CASCADE", ondelete="RESTRICT"),
            primary_key=True,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "vendor_materials",
        sa.Column(
            "vendor_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("vendors.id", onupdate="CASCADE", ondelete="RESTRICT"),
            primary_key=True,
        ),
        sa.Column(
            "material_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("materials.id", onupdate="CASCADE", ondelete="RESTRICT"),
            primary_key=True,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "vendor_brands",
        sa.Column(
            "vendor_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("vendors.id", onupdate="CASCADE", ondelete="RESTRICT"),
            primary_key=True,
        ),
        sa.Column(
            "brand_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("brands.id", onupdate="CASCADE", ondelete="RESTRICT"),
            primary_key=True,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "brand_materials",
        sa.Column(
            "brand_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("brands.id", onupdate="CASCADE", ondelete="RESTRICT"),
            primary_key=True,
        ),
        sa.Column(
            "material_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("materials.id", onupdate="CASCADE", ondelete="RESTRICT"),
            primary_key=True,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "vendor_target_groups",
        sa.Column(
            "vendor_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("vendors.id", onupdate="CASCADE", ondelete="RESTRICT"),
            primary_key=True,
        ),
        sa.Column(
            "target_group_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("target_groups.id", onupdate="CASCADE", ondelete="RESTRICT"),
            primary_key=True,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # indexes
    op.create_index("idx_vendors_city", "vendors", ["city_id"])
    op.create_index("idx_vendors_area", "vendors", ["area_id"])
    op.create_index("idx_areas_city", "areas", ["city_id"])

    op.create_index("idx_vendor_types", "vendor_vendor_types", ["vendor_type_id"])
    op.create_index("idx_vendor_materials", "vendor_materials", ["material_id"])
    op.create_index("idx_vendor_brands", "vendor_brands", ["brand_id"])
    op.create_index("idx_vendor_targets", "vendor_target_groups", ["target_group_id"])

    op.create_index(
        "idx_brand_materials_brand", "brand_materials", ["brand_id"]
    )
    op.create_index(
        "idx_brand_materials_material", "brand_materials", ["material_id"]
    )

    op.create_index(
        "idx_vendors_active", "vendors", ["is_active", "deleted_at"]
    )
    op.create_index(
        "idx_brands_active", "brands", ["is_active", "deleted_at"]
    )
    op.create_index(
        "idx_materials_active", "materials", ["is_active", "deleted_at"]
    )
    op.create_index(
        "idx_vendor_types_active", "vendor_types", ["is_active", "deleted_at"]
    )
    op.create_index(
        "idx_target_groups_active",
        "target_groups",
        ["is_active", "deleted_at"],
    )


def downgrade() -> None:
    # drop in reverse dependency order
    op.drop_index("idx_target_groups_active", table_name="target_groups")
    op.drop_index("idx_vendor_types_active", table_name="vendor_types")
    op.drop_index("idx_materials_active", table_name="materials")
    op.drop_index("idx_brands_active", table_name="brands")
    op.drop_index("idx_vendors_active", table_name="vendors")

    op.drop_index("idx_brand_materials_material", table_name="brand_materials")
    op.drop_index("idx_brand_materials_brand", table_name="brand_materials")

    op.drop_index("idx_vendor_targets", table_name="vendor_target_groups")
    op.drop_index("idx_vendor_brands", table_name="vendor_brands")
    op.drop_index("idx_vendor_materials", table_name="vendor_materials")
    op.drop_index("idx_vendor_types", table_name="vendor_vendor_types")

    op.drop_index("idx_areas_city", table_name="areas")
    op.drop_index("idx_vendors_area", table_name="vendors")
    op.drop_index("idx_vendors_city", table_name="vendors")

    op.drop_table("vendor_target_groups")
    op.drop_table("brand_materials")
    op.drop_table("vendor_brands")
    op.drop_table("vendor_materials")
    op.drop_table("vendor_vendor_types")

    op.drop_table("target_groups")
    op.drop_table("brands")
    op.drop_table("materials")
    op.drop_table("vendor_types")
    op.drop_table("vendors")
    op.drop_table("areas")
    op.drop_table("cities")

