#!/usr/bin/python3

from __future__ import annotations


class DataRange:
    def __init__(self, low: int, high: int):
        self._low = low
        self._high = high

    @property
    def getLow(self) -> int:
        return self._low

    @property
    def getHigh(self) -> int:
        return self._high

    def setLow(self, low: int):
        self._low = low % 1440

    def setHigh(self, high: int):
        self._high = high %1440


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
