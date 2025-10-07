"""initial schema

Revision ID: 0001
Revises: 
Create Date: 2024-04-19
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    fulfillment_pref = sa.Enum("in_negozio", "consegna", name="fulfillmentpref")
    fulfillment_pref.create(op.get_bind(), checkfirst=True)
    user_role = sa.Enum("user", "merchant", "admin", name="userrole")
    user_role.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("cap", sa.String(), nullable=False),
        sa.Column("fulfillment_pref", sa.Enum("in_negozio", "consegna", name="fulfillmentpref"), nullable=False),
        sa.Column("consent_geoloc", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("role", sa.Enum("user", "merchant", "admin", name="userrole"), nullable=False, server_default="user"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "store",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("chain", sa.String(), nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("cap", sa.String(), nullable=False),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("lon", sa.Float(), nullable=False),
        sa.Column("hours_json", postgresql.JSONB(), nullable=True),
        sa.Column("has_everli", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("everli_deeplink", sa.Text(), nullable=True),
        sa.Column("is_partner", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "product",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("ean", sa.String(), nullable=True),
        sa.Column("alt_codes", postgresql.JSONB(), nullable=True),
        sa.Column("brand", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("qty_value", sa.Numeric(), nullable=True),
        sa.Column("qty_unit", sa.String(), nullable=True),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("img_url", sa.Text(), nullable=True),
    )

    op.create_table(
        "sku",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("product.id"), nullable=False),
        sa.Column("store_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("store.id"), nullable=False),
        sa.Column("is_private_label", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )

    price_source = sa.Enum("volantino", "online", "scontrino", name="pricesource")
    price_source.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "price",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("sku_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sku.id"), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.Column("unit_price", sa.Numeric(), nullable=True),
        sa.Column("source_type", sa.Enum("volantino", "online", "scontrino", name="pricesource"), nullable=False),
        sa.Column("source_ref", sa.Text(), nullable=True),
        sa.Column("captured_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("valid_from", sa.Date(), nullable=True),
        sa.Column("valid_to", sa.Date(), nullable=True),
        sa.Column("confidence", sa.Integer(), nullable=True),
    )
    op.create_index("ix_price_sku_id_captured_at", "price", ["sku_id", "captured_at"], unique=False)

    op.create_table(
        "offer",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("sku_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sku.id"), nullable=False),
        sa.Column("promo_price", sa.Numeric(), nullable=False),
        sa.Column("mechanics", sa.Text(), nullable=True),
        sa.Column("start", sa.Date(), nullable=False),
        sa.Column("end", sa.Date(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
    )
    op.create_index("ix_offer_sku_id_start_end", "offer", ["sku_id", "start", "end"], unique=False)

    cart_status = sa.Enum("open", "submitted", name="cartstatus")
    cart_status.create(op.get_bind(), checkfirst=True)
    plan_kind = sa.Enum("economico", "equilibrato", "un_solo_negozio", name="plankind")
    plan_kind.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "cart",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.Enum("open", "submitted", name="cartstatus"), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "cart_item",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("cart_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cart.id"), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("product.id"), nullable=False),
        sa.Column("quantity", sa.Numeric(), nullable=False, server_default="1"),
        sa.Column("preferred_store_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("store.id"), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
    )
    op.create_index("ix_cart_item_cart_id", "cart_item", ["cart_id"], unique=False)

    op.create_table(
        "plan",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("cart_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cart.id"), nullable=False),
        sa.Column("kind", sa.Enum("economico", "equilibrato", "un_solo_negozio", name="plankind"), nullable=False),
        sa.Column("total", sa.Numeric(), nullable=False),
        sa.Column("stores_used", sa.Integer(), nullable=False),
        sa.Column("km_est", sa.Numeric(), nullable=True),
        sa.Column("details_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )

    reservation_status = sa.Enum("sent", "preparazione", "pronto", "ritirato", "annullato", name="reservationstatus")
    reservation_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "reservation",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("cart_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cart.id"), nullable=False),
        sa.Column("store_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("store.id"), nullable=False),
        sa.Column("status", sa.Enum("sent", "preparazione", "pronto", "ritirato", "annullato", name="reservationstatus"), nullable=False, server_default="sent"),
        sa.Column("pickup_code", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )

    receipt_status = sa.Enum("uploaded", "parsed", "error", name="receiptstatus")
    receipt_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "receipt",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("store_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("store.id"), nullable=False),
        sa.Column("img_url", sa.Text(), nullable=False),
        sa.Column("ocr_json", postgresql.JSONB(), nullable=True),
        sa.Column("parsed_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.Enum("uploaded", "parsed", "error", name="receiptstatus"), nullable=False, server_default="uploaded"),
    )

    op.create_table(
        "user_favorite",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("product.id"), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=True),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("user_id", "product_id", name="uq_user_product"),
    )

    op.create_table(
        "store_user",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("store_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("store.id"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("store_user")
    op.drop_table("user_favorite")
    op.drop_table("receipt")
    op.drop_table("reservation")
    op.drop_table("plan")
    op.drop_table("cart_item")
    op.drop_table("cart")
    op.drop_table("offer")
    op.drop_table("price")
    op.drop_table("sku")
    op.drop_table("product")
    op.drop_table("store")
    op.drop_table("users")

    sa.Enum(name="reservationstatus").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="receiptstatus").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="plankind").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="cartstatus").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="pricesource").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="userrole").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="fulfillmentpref").drop(op.get_bind(), checkfirst=True)
