import os
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:MYsql.db@localhost/medical_lab_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)