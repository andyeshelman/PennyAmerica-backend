from ninja import Schema
import datetime as dt

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