# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='tradinglib',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/DenerRodrigues/python-tradinglib',
    license='MIT License',
    author='Dener Rodrigues',
    author_email='dl.rodrigues94@gmail.com',
    description='Python wrapper that connects with multiple cryptocurrency exchange APIs',
    install_requires=[
        'txb-api',
        'python-binance',
        'python-bittrex',
    ],
)
