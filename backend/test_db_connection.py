"""Standalone Neon PostgreSQL connection test.

Run from the backend folder (venv active):
    python test_db_connection.py
Prints OK and the server version if the connection works.
"""
import os
import sys

# Ensure the project root is importable even when run directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

url = os.environ.get(
    'DATABASE_URL',
    'postgresql+psycopg2://neondb_owner:npg_3eVEXDdGKa9t@'
    'ep-bold-scene-aeczkuqp-pooler.c-2.us-east-2.aws.neon.tech/neondb'
    '?sslmode=require&channel_binding=require',
)

print('Connecting to:', url.split('@')[1] if '@' in url else url)

try:
    import psycopg2
    print('psycopg2 version:', psycopg2.__version__)
except ImportError as e:
    print('ERROR: psycopg2 is not installed. Run:  pip install psycopg2-binary')
    sys.exit(1)

try:
    import sqlalchemy
    from sqlalchemy import create_engine, text
    engine = create_engine(url)
    conn = engine.connect()
    result = conn.execute(text('SELECT version(), current_database()'))
    row = result.fetchone()
    print('CONNECTION OK')
    print('Database   :', row[1] if len(row) > 1 else 'n/a')
    print('PostgreSQL :', (row[0] if row else 'n/a').split(' on ')[0])
    conn.close()
except Exception as e:
    print('ERROR connecting to Neon database:')
    print('  ', type(e).__name__, '-', e)
    print()
    print('Possible causes:')
    print('  - psycopg2 not installed (run: pip install psycopg2-binary)')
    print('  - The Neon DB is paused, URL is wrong, or credentials are invalid')
    print('  - The channel_binding=require param is rejected by your libpq build')
    sys.exit(1)
