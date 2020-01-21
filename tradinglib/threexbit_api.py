# -*- coding: utf-8 -*-
from _pydecimal import Decimal

from txb_api.client import Client
from txb_api.public import Public

from .base_api import BaseAPI


class ThreeXBitAPI(BaseAPI):
    def __init__(self, api_key=None, api_secret=None):
        self._public = Public()
        self._client = self._get_client(api_key, api_secret)

    def _get_client(self, client_id, client_secret):
        try:
            return Client(client_id=client_id, client_secret=client_secret)
        except:
            return self._get_client(client_id, client_secret)

    def get_balance(self, currency: str = None):
        if currency:
            balance = self._client.balance(currency)
            return self.build_balance(
                currency=currency,
                available=balance.get('available_balance'),
                locked=balance.get('blocked_balance'),
                total=balance.get('total_balance')
            )
        balances = [
            self.build_balance(
                currency=balance.get('currency', {}).get('code'),
                available=balance.get('available_balance'),
                locked=balance.get('blocked_balance'),
                total=balance.get('total_balance')
            )
            for balance in self._client.balance()
        ]
        return balances

    def create_withdraw(self, currency: str, quantity: Decimal, address: str, tag: str = None) -> dict:
        raise NotImplemented

    def get_ticker(self, currency_price: str = 'USDT', currency_quantity: str = 'BTC'):
        market = currency_price + '_' + currency_quantity
        ticker = self._public.ticker()
        ticker = ticker.get(market)
        return self.build_ticker(
            currency_price,
            currency_quantity,
            ticker.get('last'),
            ticker.get('max'),
            ticker.get('min'),
            ticker.get('bid'),
            ticker.get('ask'),
            ticker.get('variation'),
        )

    def list_orderbook(self, currency_price: str = 'CREDIT', currency_quantity: str = 'BTC', limit: int = 10):
        book = self._public.orderbook(currency_price, currency_quantity)
        buy_orders = book.get('buy_orders')[:limit]
        sell_orders = book.get('sell_orders')[:limit]
        return buy_orders, sell_orders

    def create_order(self, order_type: str, currency_price: str, currency_quantity: str, unit_price: Decimal = None,
                     quantity: Decimal = None, execution_type: str = BaseAPI.ORDER_LIMIT) -> dict:
        return self._client.create_order(
            order_type=order_type,
            currency_price=currency_price,
            currency_quantity=currency_quantity,
            unit_price=unit_price,
            quantity=quantity,
            execution_type=execution_type,
        )

    def get_open_orders(self, currency_price: str = None, currency_quantity: str = None):
        buy_orders = self._client.list_orders(
            self._client.ORDER_BUY,
            currency_price,
            currency_quantity,
            self._client.ORDER_PENDING
        )
        sell_orders = self._client.list_orders(
            self._client.ORDER_SELL,
            currency_price,
            currency_quantity,
            self._client.ORDER_PENDING
        )
        return buy_orders, sell_orders

    def get_order_history(self, currency_price: str, currency_quantity: str):
        buy_orders = self._client.list_orders(self._client.ORDER_BUY, currency_price, currency_quantity)
        sell_orders = self._client.list_orders(self._client.ORDER_SELL, currency_price, currency_quantity)
        return buy_orders, sell_orders

    def get_order(self, order_id: str, currency_price: str = None, currency_quantity: str = None):
        return self._client.get_order(order_id)
