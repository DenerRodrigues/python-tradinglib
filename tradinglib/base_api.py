# -*- coding: utf-8 -*-

from decimal import Decimal, ROUND_DOWN


class BaseAPI:
    ORDER_BUY = 'BUY'
    ORDER_SELL = 'SELL'
    ORDER_LIMIT = 'LIMIT'
    ORDER_MARKET = 'MARKET'

    @staticmethod
    def format_decimal(value: Decimal, decimal_places: int = 8) -> Decimal:
        exp = Decimal(str('{0:.%sf}' % decimal_places).format(0))
        return value.quantize(exp, rounding=ROUND_DOWN)

    def calc_order(self, unit_price: Decimal, quantity: Decimal = None,
                   total: Decimal = None) -> (Decimal, Decimal, Decimal):
        if quantity:
            total = Decimal(str(unit_price)) * Decimal(str(quantity))
        else:
            quantity = Decimal(str(total)) / Decimal(str(unit_price))
        unit_price = self.format_decimal(unit_price)
        quantity = self.format_decimal(quantity)
        total = self.format_decimal(total)
        return unit_price, quantity, total

    @staticmethod
    def build_balance(currency, available, pending, total=None):
        if not total:
            total = Decimal(str(available)) + Decimal(str(pending))
        return {
            'currency': currency,
            'available': Decimal(str(available)),
            'pending': Decimal(str(pending)),
            'total': Decimal(str(total)),
        }

    def build_orderbook(self, unit_price, quantity, total=None):
        if not total:
            total = self.format_decimal(Decimal(str(unit_price)) * Decimal(str(quantity)))
        return {
            'unit_price': Decimal(str(unit_price)),
            'quantity': Decimal(str(quantity)),
            'total': Decimal(str(total)),
        }

    def get_balance(self, currency: str = None):
        raise NotImplementedError

    def create_withdraw(self, currency: str, quantity: Decimal, address: str, tag: str = None) -> dict:
        raise NotImplementedError

    def list_orderbook(self, currency_price: str, currency_quantity: str, limit: int = 10):
        raise NotImplementedError

    def create_order(self, order_type: str, currency_price: str, currency_quantity: str,
                     unit_price: Decimal = None, quantity: Decimal = None,
                     execution_type: str = ORDER_LIMIT) -> dict:
        raise NotImplementedError

    def get_open_orders(self, currency_price: str = None, currency_quantity: str = None):
        raise NotImplementedError

    def get_order_history(self, currency_price: str, currency_quantity: str):
        raise NotImplementedError

    def get_order(self, order_id: str, currency_price: str = None, currency_quantity: str = None):
        raise NotImplementedError
