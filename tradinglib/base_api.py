# -*- coding: utf-8 -*-

from decimal import Decimal, ROUND_DOWN


class BaseAPI:
    ORDER_BUY = 'BUY'
    ORDER_SELL = 'SELL'
    ORDER_LIMIT = 'LIMIT'
    ORDER_MARKET = 'MARKET'

    @staticmethod
    def build_balance(currency=None, available=None, pending=None, total=None):
        if not total:
            total = Decimal(str(available)) + Decimal(str(pending))
        return {
            'currency': currency,
            'available': Decimal(str(available)),
            'pending': Decimal(str(pending)),
            'total': Decimal(str(total)),
        }

    @staticmethod
    def format_decimal(value: Decimal, decimal_places: int = 8) -> Decimal:
        exp = Decimal(str('{0:.%sf}' % decimal_places).format(0))
        return value.quantize(exp, rounding=ROUND_DOWN)

    def calc_order(self, unit_price: Decimal, quantity: Decimal = None, total: Decimal = None) -> (Decimal, Decimal, Decimal):
        if quantity:
            total = Decimal(str(unit_price)) * Decimal(str(quantity))
        else:
            quantity = Decimal(str(total)) / Decimal(str(unit_price))
        unit_price = self.format_decimal(unit_price)
        quantity = self.format_decimal(quantity)
        total = self.format_decimal(total)
        return unit_price, quantity, total
