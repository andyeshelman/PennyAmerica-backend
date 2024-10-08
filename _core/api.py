from ninja import NinjaAPI
from ninja_jwt.authentication import JWTAuth

from accounts.routes import router as accounts_router
from budgets.routes import router as budgets_router
from expenses.routes import router as expenses_router
from plaids.routes import router as plaid_router
from categories.routes import router as categories_router

api = NinjaAPI(version='v0', auth=JWTAuth())

api.add_router('/accounts/', accounts_router)
api.add_router('/budgets/', budgets_router)
api.add_router('/expenses/', expenses_router)
api.add_router('/plaid/', plaid_router)
api.add_router('/categories/', categories_router)
