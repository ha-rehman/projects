from .models import UserExtension

USD_to_GBP = 0.80
USD_to_EUR = 0.90

EUR_to_USD = 1.10
EUR_to_GBP = 0.87

GBP_to_USD = 1.26
GBP_to_EUR = 1.14


def get_initial_balance(currency, initial_balance):
    if currency == UserExtension.USD:
        return initial_balance
    if currency == UserExtension.GBP:
        return initial_balance * USD_to_GBP
    if currency == UserExtension.EUR:
        return initial_balance * USD_to_EUR


def get_exchange_rate(currency1, currency2, amount):
    conversion_rates = {
        (UserExtension.USD, UserExtension.GBP): 0.80,
        (UserExtension.USD, UserExtension.EUR): 0.90,
        (UserExtension.EUR, UserExtension.USD): 1.10,
        (UserExtension.EUR, UserExtension.GBP): 0.87,
        (UserExtension.GBP, UserExtension.USD): 1.26,
        (UserExtension.GBP, UserExtension.EUR): 1.14,
    }

    rate = conversion_rates .get((currency1, currency2))
    return rate, rate * amount if rate else (None, None)
