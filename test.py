# Context

# You've received a list of user transactions, each representing a payment in a different currency. Your

# goal is to process this data and calculate the total amount spent by each user, in US dollars (USD).

# Task

# Implement a function process_transactions(transactions, exchange_rates) that:

# • Filters out invalid transactions. Consider a transaction invalid if it has a missing amount, a negative

# amount, or a currency that doesn't exist in the provided exchange rate table.

# • Converts the amount of each valid transaction to USD, using the provided exchange rate table.

# • Groups the converted amounts by user_id and returns the total spent by each user.

# • Should keep processing normally even if it encounters a malformed transaction — a problematic

# record should not interrupt the processing of the rest.

# Sample Input

transactions = [

{"user_id": 1, "amount": 50.0, "currency": "USD"},

{"user_id": 1, "amount": 30.0, "currency": "EUR"},

{"user_id": 2, "amount": -10.0, "currency": "USD"},

{"user_id": 2, "amount": 20.0, "currency": "BRL"},

{"user_id": 3, "amount": None, "currency": "USD"},

]

exchange_rates = {

"USD": 1.0,

"EUR": 1.1,

"BRL": 0.18,

}

#Expected Function Signature

def process_transactions(transactions, exchange_rates):

    totals = {}

    for transaction in transactions:
        try:
            user_id = transaction["user_id"]
            amount = transaction["amount"]
            currency = transaction["currency"]

            # Validate amount
            if amount is None or amount < 0:
                print("Invalid amount:", amount)
                continue

            # Validate currency
            if currency not in exchange_rates:
                print("Invalid currency:", currency)
                continue

            # Convert to USD
            amount_usd = amount * exchange_rates[currency]
            print("amount_usd amount_usd:", amount_usd) 

            # Aggregate by user
            totals[user_id] = totals.get(user_id, 0) + amount_usd

        except (KeyError, TypeError, ValueError):
            # Ignore malformed transactions and continue
            print("Malformed transaction:", transaction)
            continue

    return totals


# Example call:

result = process_transactions(transactions, exchange_rates)

print(result)