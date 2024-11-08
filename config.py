import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def create_sqlite_uri(db_name):
    return "sqlite:///" + os.path.join(BASEDIR, db_name)

def create_mssql_uri(username, password, server, port, database):
    return f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver=ODBC+Driver+18+for+SQL+Server"



class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret key, just for testing"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri("todolist-dev.db")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri("todolist-test.db")
    WTF_CSRF_ENABLED = False
    import logging

    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    logging.getLogger().setLevel(logging.DEBUG)


class ProductionConfig(Config):
    # Використання MSSQL у Production
    SQLALCHEMY_DATABASE_URI = create_mssql_uri("admin", "admin1234", "database-1.cvg2a0y6kojy.us-east-1.rds.amazonaws.com", "Lab3Cloud")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
