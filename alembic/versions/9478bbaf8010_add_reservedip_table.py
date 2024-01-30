"""add reservedip table

Revision ID: 9478bbaf8010
Revises: 6627b128bd5c
Create Date: 2019-10-14 12:21:25.619884

"""
import sqlalchemy as sa
import sqlalchemy_utils

from alembic import op

# revision identifiers, used by Alembic.
revision = "9478bbaf8010"
down_revision = "6627b128bd5c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "reservedip",
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("ip", sqlalchemy_utils.types.ip_address.IPAddressType(length=50), nullable=True),
        sa.Column("last_seen", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["device_id"],
            ["device.id"],
        ),
        sa.PrimaryKeyConstraint("device_id"),
    )
    op.create_index(op.f("ix_reservedip_device_id"), "reservedip", ["device_id"], unique=False)
    op.create_unique_constraint(None, "joblock", ["jobid"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "joblock", type_="unique")
    op.drop_index(op.f("ix_reservedip_device_id"), table_name="reservedip")
    op.drop_table("reservedip")
    # ### end Alembic commands ###
