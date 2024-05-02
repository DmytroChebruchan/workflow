"""Creating table

Revision ID: 775db83515ca
Revises: 
Create Date: 2024-05-02 14:22:24.826893

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "775db83515ca"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "workflows",
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "nodes",
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("message_text", sa.String(), nullable=True),
        sa.Column("condition", sa.String(), nullable=True),
        sa.Column("workflow_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["workflow_id"],
            ["workflows.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "edges",
        sa.Column("source_node_id", sa.Integer(), nullable=True),
        sa.Column("destination_node_id", sa.Integer(), nullable=True),
        sa.Column("condition_type", sa.Boolean(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["destination_node_id"],
            ["nodes.id"],
        ),
        sa.ForeignKeyConstraint(
            ["source_node_id"],
            ["nodes.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("edges")
    op.drop_table("nodes")
    op.drop_table("workflows")
    # ### end Alembic commands ###
