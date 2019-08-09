# -*- coding: utf-8 -*-

from txb_api.client import Client
from txb_api.public import Public


class ThreeXBitAPI:
    def __init__(self, api_key=None, api_secret=None):
        self._public = Public()
        self._client = self._get_client(api_key, api_secret)

    def _get_client(self, client_id, client_secret):
        try:
            return Client(client_id=client_id, client_secret=client_secret)
        except:
            return self._get_client(client_id, client_secret)

    def list_orderbook(self, currency_price: str ='CREDIT', currency_quantity: str = 'BTC', limit: int = 10):
        book = self._public.orderbook(currency_price, currency_quantity)
        buy_orders = book.get('buy_orders')[:limit]
        sell_orders = book.get('sell_orders')[:limit]
        return buy_orders, sell_orders
