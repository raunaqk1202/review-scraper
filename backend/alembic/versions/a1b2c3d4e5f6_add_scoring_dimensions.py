"""add scoring dimensions

Revision ID: a1b2c3d4e5f6
Revises: 3f7f0b01e12a
Create Date: 2026-08-28 03:36:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '3f7f0b01e12a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns
    op.add_column('opportunity_score', sa.Column('user_pain', sa.Float(), nullable=True))
    
    # Drop old unused columns
    # Using batch_alter_table to support both SQLite and Postgres
    with op.batch_alter_table('opportunity_score', schema=None) as batch_op:
        batch_op.drop_column('frequency')
        batch_op.drop_column('severity')
        batch_op.drop_column('cross_source_consistency')
        batch_op.drop_column('cross_segment_relevance')
        batch_op.drop_column('trend_score')
        batch_op.drop_column('strategic_relevance')


def downgrade() -> None:
    with op.batch_alter_table('opportunity_score', schema=None) as batch_op:
        batch_op.add_column(sa.Column('strategic_relevance', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('trend_score', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('cross_segment_relevance', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('cross_source_consistency', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('severity', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('frequency', sa.FLOAT(), nullable=True))
        batch_op.drop_column('user_pain')
