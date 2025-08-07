"""prepopulate table

Revision ID: c9edc85a981e
Revises: a1399ebb2773
Create Date: 2025-08-07 12:42:52.322665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9edc85a981e'
down_revision: Union[str, Sequence[str], None] = 'a1399ebb2773'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


data = [
    "'To Kill a Mockingbird', 'Harper Lee', 324, 4.8, 14.99",
    "'1984', 'George Orwell', 328, 4.7, 12.95",
    "'Animal Farm', 'George Orwell', 112, 4.6, 8.99",
    "'Pride and Prejudice', 'Jane Austen', 279, 4.6, 9.99",
    "'The Great Gatsby', 'F. Scot Fitzgerald', 180, 4.4, 10.99",
]


def upgrade() -> None:
    """Upgrade schema."""
    for b in data:
        op.execute(sa.text(f"""INSERT INTO books
            (title, author, pages, rating, price)
            VALUES ({b});
        """)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""TRUNCATE TABLE books;""")
