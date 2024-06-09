"""empty message

Revision ID: 91e8574a2111
Revises: 6cef8252083f
Create Date: 2024-06-09 17:41:17.942984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91e8574a2111'
down_revision = '6cef8252083f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('imagem', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('imagem')

    # ### end Alembic commands ###
