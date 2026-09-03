import os
from sqlalchemy.pool import StaticPool

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../database'))
DB_PATH = os.path.join(DB_DIR, 'hr_platform.db')
UPLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR, '../uploads/resumes'))

makedirs = os.makedirs
makedirs(DB_DIR, exist_ok=True)
makedirs(UPLOAD_DIR, exist_ok=True)

DEFAULT_DATABASE_URL = 'postgresql+psycopg2://neondb_owner:npg_3eVEXDdGKa9t@ep-bold-scene-aeczkuqp-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-hr-platform-secret-key-32chars!'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-dev-key-for-hr-platform-secret-32chars!'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or DEFAULT_DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or UPLOAD_DIR
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'poolclass': StaticPool,
        'connect_args': {'check_same_thread': False}
    }
    JWT_SECRET_KEY = 'test-jwt-secret-very-secure-32-chars-long-key!'
