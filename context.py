#!/usr/bin/env python
# coding=utf-8


class Context(object):
    _data = {}

    @classmethod
    def get(cls, key):
        return cls._data.get(key)

    @classmethod
    def set(cls, key, value):
        cls._data[key] = value


current_ctx = Context
