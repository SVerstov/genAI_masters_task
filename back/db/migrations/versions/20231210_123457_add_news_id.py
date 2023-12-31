"""'add_news_id'

Revision ID: e74df7029c11
Revises: fa6b01f01d6c
Create Date: 2023-12-10 12:34:57.699448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e74df7029c11'
down_revision = 'fa6b01f01d6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('news_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix__news_news_id'), 'news', ['news_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix__news_news_id'), table_name='news')
    op.drop_column('news', 'news_id')
    # ### end Alembic commands ###
