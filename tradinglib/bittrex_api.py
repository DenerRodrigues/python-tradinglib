# -*- coding: utf-8 -*-

from decimal import Decimal

from bittrex.bittrex import API_V2_0, Bittrex as Client


class BittrexAPI:
    def __init__(self, currency_price='USDT', currency_quantity='BTC', api_key=None, api_secret=None):
        self.market = currency_price + '-' + currency_quantity
        self.currency_price = currency_price
        self.currency_quantity = currency_quantity
        self._client = self._get_client(api_key, api_secret)

    def _get_client(self, api_key, api_secret):
        try:
            return Client(api_key=api_key, api_secret=api_secret, api_version=API_V2_0)
        except:
            return self._get_client(api_key, api_secret)

    def list_orderbook(self, only_prices=False, limit=10):
        book = self._client.get_orderbook(market=self.market).get('result')
        book_buy_orders = book.get('buy')[:limit]
        book_sell_orders = book.get('sell')[:limit]
        if only_prices:
            book_buy_orders = [Decimal(str(order.get('Rate'))) for order in book_buy_orders]
            book_sell_orders = [Decimal(str(order.get('Rate'))) for order in book_sell_orders]
        return book_buy_orders, book_sell_orders
