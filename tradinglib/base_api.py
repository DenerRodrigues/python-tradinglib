# -*- coding: utf-8 -*-

from decimal import Decimal


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
