## Creation Steps

1. Create empty folder `PennyAmerica-backend`, cd into it and run `code .`
2. Create and activate virtual environment
   1. `python3 -m venv venv`
   2. `. venv/bin/activate`
3. Run
   1. `pip install -U pip`
   2. `pip install django django-ninja "psycopg[binary]"`
   3. `pip freeze > requirements.txt`
4. Run `django-admin startproject "_core" .`
5. Change the `DATABASES` variable in `_core/settings.py`
6. Initialize database with `python3 manage.py migrate`
7. Create admin account with `python3 manage.py createsuperuser`
8. Initialize expenses app with `python3 manage.py startapp expenses`
9. Add `'expenses'` to `INSTALLED_APPS` in `_core/settings.py`
10. Add `Expense` model to `expenses/models.py`
11. Register model in `expenses/admin.py`
12. Update database
    1.  `python3 manage.py makemigrations`
    2.  `python3 manage.py migrate`
13. Initialize accounts app with `python3 manage.py startapp accounts`
14. Add `'accounts'` to `INSTALLED_APPS` in `_core/settings.py`
15. Add `schemas.py` to `expenses/` and `accounts/` and write schemas
16. Add `api` folder to `expenses/` and `accounts/`
17. Add `routes.py` file to `api` folder and initialize routers
18. Add `api.py` to `_core/`, initialize api, and register routers
19. Add api to `urlpatterns` in `_core/urls.py`