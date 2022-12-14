"""delete unused fields

Revision ID: e9bd6dbd0a08
Revises: 5d71a571b9d3
Create Date: 2022-11-08 06:34:32.716664

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e9bd6dbd0a08'
down_revision = '5d71a571b9d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_avatar_key', 'user', type_='unique')
    op.drop_column('user', 'passport_id')
    op.drop_column('user', 'weight')
    op.drop_column('user', 'instagram_url')
    op.drop_column('user', 'is_superuser')
    op.drop_column('user', 'height')
    op.drop_column('user', 'uae_id')
    op.drop_column('user', 'zip_code')
    op.drop_column('user', 'state')
    op.drop_column('user', 'bust_type')
    op.drop_column('user', 'avatar')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('bust_type', postgresql.ENUM('NATURAL', 'IMPLANTS', name='busttype'), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('state', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('zip_code', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('uae_id', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('height', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('instagram_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('weight', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('passport_id', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.create_unique_constraint('user_avatar_key', 'user', ['avatar'])
    # ### end Alembic commands ###
