from dependency_injector import containers, providers

from users.domain.use_cases import (
    AuthenticateUserCase,
    GetUserCase,
    RegisterUserCase,
    CreateAccessTokenCase,
    CreateRefreshTokenCase,
    DecodeTokenCase,
    UpdateUserCase,
)


class UseCasesContainer(containers.DeclarativeContainer):
    repos = providers.DependenciesContainer()

    authenticate_user_uc = providers.Factory(AuthenticateUserCase, repository=repos.user_repository)
    get_user_uc = providers.Factory(GetUserCase, repository=repos.user_repository)
    register_user_uc = providers.Factory(RegisterUserCase, repository=repos.user_repository)
    update_user_uc = providers.Factory(UpdateUserCase, repository=repos.user_repository)

    create_access_token_uc = providers.Factory(
        CreateAccessTokenCase, repository=repos.token_repository
    )
    create_refresh_token_uc = providers.Factory(
        CreateRefreshTokenCase, repository=repos.token_repository
    )
    decode_token_uc = providers.Factory(DecodeTokenCase, repository=repos.token_repository)
