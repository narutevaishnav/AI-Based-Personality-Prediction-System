"""
Ha script ekdach chalvaycha aahe — 'predictions' table madhe
'input_text' navachi navin column add karnya sathi.

Vaparaycha: tuza project cha root folder madhe hi file
'add_column.py' navane save kar, ani terminal madhe:

    python add_column.py

chalav. Ek success message distel.
"""

from app import app
from models import db
from sqlalchemy import text

with app.app_context():

    with db.engine.connect() as connection:

        connection.execute(
            text(
                "ALTER TABLE predictions ADD COLUMN IF NOT EXISTS input_text TEXT;"
            )
        )

        connection.commit()

    print("SUCCESS: 'input_text' column tuza 'predictions' table madhe add zali!")  