from dependency_injector import containers, providers

from containers.gateways_container import Gateways
from containers.repos_container import ReposContainer
from containers.use_cases_container import UseCasesContainer
from core.config import get_settings

app_config = get_settings()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[app_config])
    wiring_config = containers.WiringConfiguration(
        packages=["users.api.endpoints", "users.dependencies"]
    )
    gateways = providers.Container(Gateways, config=config)
    repos = providers.Container(ReposContainer, gateways=gateways)
    use_cases = providers.Container(UseCasesContainer, repos=repos)


container = Container()
