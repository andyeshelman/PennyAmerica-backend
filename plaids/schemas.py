from ninja import Schema, Field

import datetime as dt
from typing import Any

from util.schemas import Lift

class ItemIDSchema(Schema):
    item_id: str

class CounterpartySchema(Schema):
    name: str
    type: Lift[str]
    website: str | None
    logo_url: str | None
    confidence_level: str | None
    entity_id: str | None
    phone_number: str | None

class LocationSchema(Schema):
    address: str | None
    city: str| None
    region: str | None
    postal_code: str | None
    country: str | None
    lat: float | None
    lon: float | None
    store_number: str | None

class PaymentMetaSchema(Schema):
    reference_number: str | None
    ppd_id: str | None
    payee: str | None
    by_order_of: str | None
    payer: str | None
    payment_method: str | None
    payment_processor: str | None
    reason: str | None

class PersonalFinanceCategorySchema(Schema):
    confidence_level: str | None
    detailed: str
    primary: str

class TransactionSchema(Schema):
    account_id: str
    account_owner: str | None
    amount: float
    authorized_date: dt.date | None
    authorized_datetime: dt.datetime | None
    category: list[str] | None
    category_id: str | None
    check_number: str | None
    counterparties: list[CounterpartySchema]
    date: dt.date
    datetime: dt.datetime | None
    iso_currency_code: str | None
    location: LocationSchema
    logo_url: str | None
    merchant_entity_id: str | None
    merchant_name: str | None
    name: str
    payment_channel: str
    payment_meta: PaymentMetaSchema
    pending: bool
    pending_transaction_id: str | None
    personal_finance_category: PersonalFinanceCategorySchema
    personal_finance_category_icon_url: str
    transaction_code: Lift[str] | None
    transaction_id: str
    transaction_type: str
    unofficial_currency_code: str | None
    website: str | None
    
class TransactionResponseSchema(Schema):
    transactions: list[TransactionSchema]

class LinkTokenResponseSchema(Schema):
    link_token: str
    expiration: dt.datetime
    request_id: str

class SPTCRequestSchema(Schema):
    institution_id: str = Field(..., example='ins_109508')
    username: str = Field(..., example='user_transactions_dynamic')
    password: str = Field(..., example='pass_good')

class InstitutionSchema(Schema):
    institution_id: str
    name: str
    products: list[str]
    country_codes: list[str]
    routing_numbers: list[str]
    oauth: bool

class InstitutionResponseSchema(Schema):
    institution: InstitutionSchema
    request_id: str

class AccountBalanceSchema(Schema):
    available: float | None
    current: float | None
    limit: float | None
    iso_currency_code: str | None
    unofficial_currency_code: str | None
    last_updated_datetime: dt.datetime | None = None

class AccountBaseSchema(Schema):
    account_id: str
    balances: AccountBalanceSchema
    mask: str | None
    name: str
    official_name: str | None
    type: str
    subtype: str | None
    persistent_account_id: str | None = None

class PlaidErrorSchema(Schema):
    error_type: Lift[str]
    error_code: str
    error_message: str
    display_message: str | None
    request_id: str
    causes: list[Any]
    status: int | None
    documentation_url: str
    suggested_action: str | None

class ItemSchema(Schema):
    item_id: str
    webhook: str | None
    error: PlaidErrorSchema | None
    available_products: list[str]
    billed_products: list[str]
    consent_expiration_time: dt.datetime | None
    update_type: str
    institution_id: str | None
    products: list[str]

class AuthGetResponseSchema(Schema):
    accounts: list[AccountBaseSchema]
    numbers: dict
    item: ItemSchema
    request_id: str

class AuthResponseSchema(Schema):
    auths: list[AuthGetResponseSchema]
