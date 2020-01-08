# -*- coding: utf-8 -*-

from decimal import Decimal

from binance.client import Client

from .base_api import BaseAPI


class BinanceAPI(BaseAPI):
    def __init__(self, api_key=None, api_secret=None):
        self._client = self._get_client(api_key, api_secret)
        self.recv_window = 1000

    @staticmethod
    def _get_client(api_key, api_secret):
        return Client(api_key=api_key, api_secret=api_secret)

    def get_balance(self, currency: str = None):
        if currency:
            balance = self._client.get_asset_balance(currency, **{'recvWindow': self.recv_window})
            return self.build_balance(
                currency=balance.get('asset'),
                available=balance.get('free'),
                pending=balance.get('locked')
            )
        balances = [
            self.build_balance(
                currency=balance.get('asset'),
                available=balance.get('free'),
                pending=balance.get('locked')
            )
            for balance in self._client.get_account(**{'recvWindow': self.recv_window}).get('balances')
        ]
        return balances

    def create_withdraw(self, currency: str, quantity: Decimal, address: str, tag: str = None) -> dict:
        params = {
            'asset': currency,
            'amount': quantity,
            'address': address,
            'recvWindow': self.recv_window,
        }
        if tag:
            params['addressTag'] = tag

        withdraw = self._client.withdraw(**params)
        return withdraw

    def get_ticker(self, currency_price: str = 'USDT', currency_quantity: str = 'BTC'):
        symbol = currency_quantity + currency_price
        ticker = self._client.get_ticker(symbol=symbol)
        return self.build_ticker(
            ticker.get('lastPrice'),
            ticker.get('highPrice'),
            ticker.get('lowPrice'),
            ticker.get('bidPrice'),
            ticker.get('askPrice'),
            ticker.get('priceChangePercent'),
        )

    def list_orderbook(self, currency_price: str = 'USDT', currency_quantity: str = 'BTC', limit: int = 10):
        symbol = currency_quantity + currency_price
        book = self._client.get_order_book(symbol=symbol)

        buy_orders = book.get('bids')[:limit]
        buy_orders = [self.build_orderbook(order[0], order[1]) for order in buy_orders]

        sell_orders = book.get('asks')[:limit]
        sell_orders = [self.build_orderbook(order[0], order[1]) for order in sell_orders]

        return buy_orders, sell_orders

    def create_order(self, order_type: str, currency_price: str, currency_quantity: str,
                     unit_price: Decimal = None, quantity: Decimal = None,
                     execution_type: str = BaseAPI.ORDER_LIMIT) -> dict:
        order = {}
        symbol = currency_quantity + currency_price
        params = {
            'symbol': symbol,
            'price': unit_price,
            'recvWindow': self.recv_window,
        }
        if execution_type == self.ORDER_LIMIT:
            if order_type == self.ORDER_BUY:
                params['quantity'] = quantity
                order = self._client.order_limit_buy(**params)
            elif order_type == self.ORDER_SELL:
                params['quantity'] = quantity
                order = self._client.order_limit_sell(**params)
        return order

    def get_open_orders(self, currency_price: str = None, currency_quantity: str = None):
        params = {
            'recvWindow': self.recv_window,
        }
        if currency_price and currency_quantity:
            symbol = currency_quantity + currency_price
            params['symbol'] = symbol
        orders = self._client.get_open_orders(**params)
        return orders

    def get_order_history(self, currency_price: str, currency_quantity: str):
        symbol = currency_quantity + currency_price
        params = {
            'symbol': symbol,
            'recvWindow': self.recv_window,
        }
        orders = self._client.get_all_orders(**params)
        return orders

    def get_order(self, order_id: str, currency_price: str = None, currency_quantity: str = None):
        symbol = currency_quantity + currency_price
        params = {
            'symbol': symbol,
            'orderId': order_id,
            'recvWindow': self.recv_window,
        }
        order = self._client.get_order(**params)
        return order
