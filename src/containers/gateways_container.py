from dependency_injector import containers, providers

from core.db.db import Database


class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Singleton(Database, config.database.sqlalchemy_database_uri)
