"""add collection value field

Revision ID: c4462f0b54c9
Revises: 35c42c42d58b
Create Date: 2021-06-28 16:40:34.746137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4462f0b54c9'
down_revision = '35c42c42d58b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('name',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('count',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('collection', schema=None) as batch_op:
        batch_op.add_column(sa.Column('value', sa.Float(), nullable=True))
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('name',
               existing_type=sa.TEXT(),
               nullable=False)

    with op.batch_alter_table('collection_card_rel', schema=None) as batch_op:
        batch_op.alter_column('collection_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('card_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_index('idx_collection_card_rel_card_id')
        batch_op.drop_index('idx_collection_card_rel_collection_id')

    with op.batch_alter_table('price', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('card_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('date',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.drop_index('idx_price_card_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('price', schema=None) as batch_op:
        batch_op.create_index('idx_price_card_id', ['card_id'], unique=False)
        batch_op.alter_column('date',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('card_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    with op.batch_alter_table('collection_card_rel', schema=None) as batch_op:
        batch_op.create_index('idx_collection_card_rel_collection_id', ['collection_id'], unique=False)
        batch_op.create_index('idx_collection_card_rel_card_id', ['card_id'], unique=False)
        batch_op.alter_column('card_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('collection_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('collection', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
        batch_op.drop_column('value')

    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.alter_column('count',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    # ### end Alembic commands ###
