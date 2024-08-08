from ninja import NinjaAPI

from accounts.api.routes import router as accounts_router
from expenses.api.routes import router as expenses_router

api = NinjaAPI(version="v0")

api.add_router("/accounts/", accounts_router)
api.add_router("/expenses/", expenses_router)