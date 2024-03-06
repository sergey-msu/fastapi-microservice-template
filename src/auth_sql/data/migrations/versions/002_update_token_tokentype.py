'''
WARNING: Do not change anything here.
         Just copy the file and change its name from [N]_prev.py to [N+1]_next.py
'''
import os

from alembic import op


path = os.path.abspath(os.path.dirname(__file__))
script = os.path.basename(__file__).split('.')[0]

revision = script.split('_')[0]
down_revision = None if revision == '000' else str(int(revision) - 1).zfill(3)
branch_labels = None
depends_on = None


def upgrade() -> None:
    with open(f'{path}/../scripts/{script}.sql', 'r') as file:
        op.execute(file.read())


def downgrade() -> None:
    raise NotImplementedError
