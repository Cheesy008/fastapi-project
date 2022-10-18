# Import all the models, so that Base has them before being
# imported by Alembic
from core.db.base_class import Base  # noqa
from users.data.models import BlacklistToken, OutstandingToken  # noqa
from users.data.models import User  # noqa
