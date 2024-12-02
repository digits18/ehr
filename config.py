import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    SQLALCHEMY_DATABASE_URI = os.getenv('Database_URL', 'postgresql://neondb_owner:KaD0Hu4FvNQw@ep-snowy-salad-a4vt4d43-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
