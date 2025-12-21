# Make a currency converter using real exchange rates

import requests

def get_exchange_rate(from_currency, to_currency):
    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['result'] == 'success':
            rates = data['rates']
            if to_currency in rates:
                return rates[to_currency]
            else:
                print(f"Currency '{to_currency}' not supported.")
                return None
        else:
            print("Failed to fetch exchange rates.")
            return None
    except requests.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None

def convert_currency(amount, from_currency, to_currency):
    rate = get_exchange_rate(from_currency.upper(), to_currency.upper())
    if rate:
        converted_amount = amount * rate
        return converted_amount
    else:
        return None

if __name__ == "__main__":
    from_curr = input("Enter source currency code (e.g., USD): ").strip().upper()
    to_curr = input("Enter target currency code (e.g., INR): ").strip().upper()
    try:
        amount = float(input(f"Enter amount in {from_curr}: "))
    except ValueError:
        print("Invalid amount input.")
        exit(1)

    result = convert_currency(amount, from_curr, to_curr)
    if result is not None:
        print(f"{amount:.2f} {from_curr} = {result:.2f} {to_curr}")
    else:
        print("Conversion failed.")
