"""Made hashed_password nullable

Revision ID: 2b825fd09468
Revises: d05d5d2597a1
Create Date: 2024-10-09 22:07:20.251482

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2b825fd09468"
down_revision: Union[str, None] = "d05d5d2597a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # SQLite workaround for altering columns
    # Step 1: Create a new table with the updated schema
    op.create_table(
        "user_new",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column(
            "hashed_password", sa.String(), nullable=True
        ),  # Make hashed_password nullable
        sa.Column("issued_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Step 2: Copy data from the old table to the new table
    op.execute(
        'INSERT INTO user_new (id, created, username, email, hashed_password, issued_at) SELECT "user".id, "user".created, "user".username, "user".email, "user".hashed_password, "user".issued_at FROM "user";'
    )

    # Step 3: Drop the old table
    op.drop_table("user")

    # Step 4: Rename the new table to the old table name
    op.rename_table("user_new", "user")


def downgrade() -> None:
    # Revert changes by recreating the original table with non-nullable hashed_password
    op.create_table(
        "user_old",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column(
            "hashed_password", sa.String(), nullable=False
        ),  # Make hashed_password non-nullable again
        sa.Column("issued_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Copy data back from the current table to the old table
    op.execute(
        "INSERT INTO user_old (id, created, username, email, hashed_password, issued_at) SELECT id, created, username, email, hashed_password, issued_at FROM user"
    )

    # Drop the current table
    op.drop_table("user")

    # Rename the old table back to the original name
    op.rename_table("user_old", "user")
