import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../database'))
DB_PATH = os.path.join(DB_DIR, 'hr_platform.db')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-hr-platform'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-dev-key-for-hr-platform'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.abspath(os.path.join(BASE_DIR, '../uploads/resumes'))
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
