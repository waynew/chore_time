"""Create family member table

Revision ID: 51b8693f1a7
Revises: None
Create Date: 2014-02-02 13:12:25.927855

"""

# revision identifiers, used by Alembic.
revision = '51b8693f1a7'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
            'family',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String, nullable=False),
            )

    op.create_table(
            'family_member',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String, nullable=False),
            sa.Column('email', sa.String, nullable=True),
            sa.Column('family', sa.Integer, sa.ForeignKey('family.id')),
            )


def downgrade():
    op.drop_table('family_member')
    op.drop_table('family')
