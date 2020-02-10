# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal, ROUND_DOWN


class BaseAPI:
    ORDER_BUY = 'BUY'
    ORDER_SELL = 'SELL'
    ORDER_LIMIT = 'LIMIT'
    ORDER_MARKET = 'MARKET'

    @staticmethod
    def format_number(value, decimal_places=8) -> Decimal:
        exp = Decimal(str('{0:.%sf}' % decimal_places).format(0))
        return Decimal(str(value)).quantize(exp, rounding=ROUND_DOWN)

    def calc_order(self, unit_price: Decimal,
                   quantity: Decimal = None, total: Decimal = None) -> (Decimal, Decimal, Decimal):
        if quantity:
            total = Decimal(str(unit_price)) * Decimal(str(quantity))
        else:
            quantity = Decimal(str(total)) / Decimal(str(unit_price))
        unit_price = self.format_number(unit_price)
        quantity = self.format_number(quantity)
        total = self.format_number(total)
        return unit_price, quantity, total

    def build_balance(self, currency, available, locked, total=None):
        if not total:
            total = Decimal(str(available)) + Decimal(str(locked))
        return {
            'currency': currency,
            'available': self.format_number(available),
            'locked': self.format_number(locked),
            'total': self.format_number(total),
        }

    def build_ticker(self, currency_price, currency_quantity, last_price, high_price, low_price, bid_price, ask_price, variation):
        return {
            'market': '{}-{}'.format(currency_quantity, currency_price),
            'last': self.format_number(last_price),
            'high': self.format_number(high_price),
            'low': self.format_number(low_price),
            'bid': self.format_number(bid_price),
            'ask': self.format_number(ask_price),
            'variation': self.format_number(variation),
        }

    def build_orderbook(self, unit_price, quantity, total=None):
        if not total:
            total = Decimal(str(unit_price)) * Decimal(str(quantity))
        return {
            'unit_price': self.format_number(unit_price),
            'quantity': self.format_number(quantity),
            'total': self.format_number(total),
        }

    def build_order(self, order_id, order_type, currency_price, currency_quantity,
                    unit_price, quantity, executed, status, time):
        return {
            'order_id': order_id,
            'order_type': order_type,
            'market': '{}-{}'.format(currency_quantity, currency_price),
            'unit_price': self.format_number(unit_price),
            'quantity': self.format_number(quantity),
            'executed': self.format_number(executed),
            'status': status,
            'time': datetime.fromtimestamp(int(str(time)[:10])),
        }

    def get_ticker(self, currency_price: str, currency_quantity: str):
        raise NotImplementedError

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

    def cancel_order(self, order_id: str, currency_price: str = None, currency_quantity: str = None):
        raise NotImplementedError
