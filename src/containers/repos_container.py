from dependency_injector import containers, providers

from users.data.repositories.token_repository import TokenRepository
from users.data.repositories.user_repository import UserRepository


class ReposContainer(containers.DeclarativeContainer):
    gateways = providers.DependenciesContainer()

    token_repository = providers.Factory(
        TokenRepository, session_factory=gateways.db.provided.get_session
    )
    user_repository = providers.Factory(
        UserRepository, session_factory=gateways.db.provided.get_session
    )
