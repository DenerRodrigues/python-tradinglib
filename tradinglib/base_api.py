# -*- coding: utf-8 -*-

from decimal import Decimal


class BaseAPI:
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
