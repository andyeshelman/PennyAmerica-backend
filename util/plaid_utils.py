import plaid
from plaid.model.accounts_get_request import AccountsGetRequest
from plugins.plaid import client

def filter_transactions(transactions, plaids, allowed_account_names, excluded_account_names):
    account_mapping = {}
    processed_tokens = set()

    for plaid_instance in plaids:
        if plaid_instance.access_token in processed_tokens:
            continue

        try:
            accounts_get_request = AccountsGetRequest(access_token=plaid_instance.access_token)
            response = client.accounts_get(accounts_get_request)
            for account in response['accounts']:
                account_mapping[account['account_id']] = account['name']
            processed_tokens.add(plaid_instance.access_token)
        except plaid.ApiException:
            continue

    filtered_transactions = []

    for txn in transactions:
        account_name = account_mapping.get(txn['account_id'])

        if account_name in excluded_account_names:
            continue

        if account_name in allowed_account_names:
            if txn['category'] == ['Payment'] and account_name in allowed_account_names:
                if "Credit Card" in txn['category'] and txn['name'].lower().startswith('credit card') and txn['personal_finance_category']['detailed'] == 'LOAN_PAYMENTS_CREDIT_CARD_PAYMENT':
                    filtered_transactions.append(txn)
                else:
                    continue
            else:
                filtered_transactions.append(txn)

    final_filtered_transactions = []
    for transaction in filtered_transactions:
        category = transaction.get("category", [])
        transaction_type = transaction.get("transaction_type", "")
        name = transaction.get("name", "").lower()
        detailed_category = transaction.get('personal_finance_category', {}).get('detailed', '')

        if category and "Payment" in category and "Credit Card" in category:
            if transaction_type == "special" and detailed_category != 'LOAN_PAYMENTS_CREDIT_CARD_PAYMENT':
                continue
            if "payment" in name and detailed_category != 'LOAN_PAYMENTS_CREDIT_CARD_PAYMENT':
                continue

        final_filtered_transactions.append(transaction)

    return final_filtered_transactions