"""
Project: NishadRaj OS
Organization: AITDL | NISHADRAJ
Organization: AITDL
License: AGPL-3.0 + Governance Protection
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c735a8cb2b4e'
down_revision: Union[str, Sequence[str], None] = 'cf38d4a4928d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Note: users table might already exist if f3902bb17ca2 was applied.
    # In a governed migration review, we show the targeted state.
    
    # Check for existing table if needed, but for --sql output we want the statements.
    
    # 1. Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('module', sa.String(length=100), nullable=False, server_default='AUTH'),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. Ensure users table has all AUTH_002 fields (Account Locking)
    # This is often done via add_column if table exists.
    # We add columns for institutional ready security.
    op.add_column('users', sa.Column('account_locked', sa.Boolean(), nullable=False, server_default=sa.text('false')))


def downgrade() -> None:
    op.drop_column('users', 'account_locked')
    op.drop_table('audit_logs')
