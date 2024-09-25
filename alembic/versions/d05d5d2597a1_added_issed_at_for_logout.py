"""Added issed_at for logout

Revision ID: d05d5d2597a1
Revises: 7b8c8514f31f
Create Date: 2024-09-18 11:48:25.898597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd05d5d2597a1'
down_revision: Union[str, None] = '7b8c8514f31f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('issued_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'issued_at')
    # ### end Alembic commands ###
