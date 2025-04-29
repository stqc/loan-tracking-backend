import os
from datetime import timedelta

db_path = os.path.join(os.path.dirname(__file__), "test.db")

configs = {
    "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "JWT_SECRET_KEY":"some_super_secret_key",
    'JWT_TOKEN_LOCATION' : ['cookies'],
    "JWT_COOKIE_SECURE": False,
    "JWT_COOKIE_CSRF_PROTECT" : True,
    "JWT_ACCESS_TOKEN_EXPIRES": timedelta(days=1),
    "JWT_REFRESH_TOKEN_EXPIRES": timedelta(days=30),
}