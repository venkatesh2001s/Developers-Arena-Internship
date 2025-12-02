#Build a currency converter with multiple functions

# Dictionary with currency exchange rates relative to USD
exchange_rates = {
    "USD": 1.0,
    "INR": 83.25,
    "EUR": 0.91,
    "GBP": 0.79,
    "JPY": 149.5,
    "AUD": 1.49
}

def get_exchange_rate(from_currency, to_currency):
    """Get the exchange rate from one currency to another"""
    if from_currency not in exchange_rates or to_currency not in exchange_rates:
        return None
    # Convert from source currency to USD, then USD to target currency
    rate = exchange_rates[to_currency] / exchange_rates[from_currency]
    return rate

def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another"""
    rate = get_exchange_rate(from_currency, to_currency)
    if rate is None:
        return None
    return amount * rate

def format_currency(amount, currency):
    """Format the amount with currency symbol (simple)"""
    symbols = {
        "USD": "$",
        "INR": "₹",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "AUD": "A$"
    }
    symbol = symbols.get(currency, "")
    return f"{symbol}{amount:,.2f}"

def main():
    print("Welcome to the Developer's Arena Currency Converter")

    from_currency = input("Enter source currency code (e.g., USD): ").upper()
    to_currency = input("Enter target currency code (e.g., INR): ").upper()
    try:
        amount = float(input(f"Enter amount in {from_currency}: "))
    except ValueError:
        print("Invalid amount entered.")
        return

    converted_amount = convert_currency(amount, from_currency, to_currency)
    if converted_amount is None:
        print("Invalid currency code entered.")
        return

    formatted_original = format_currency(amount, from_currency)
    formatted_converted = format_currency(converted_amount, to_currency)

    print(f"{formatted_original} is equivalent to {formatted_converted}.")

if __name__ == "__main__":
    main()
