from ninja import NinjaAPI
from ninja_jwt.authentication import JWTAuth

from accounts.api.routes import router as accounts_router
from expenses.api.routes import router as expenses_router
from plaids.api.routes import router as plaid_router

api = NinjaAPI(version="v0", auth=JWTAuth())

api.add_router("/accounts/", accounts_router)
api.add_router("/expenses/", expenses_router)
api.add_router("/plaid/", plaid_router)
