#!/usr/bin/env python
# coding=utf-8

import yaml


class Meta(type):
    def __new__(cls, classname, bases, classdict):
        try:
            with open(classdict['CONFIG_PATH']) as file:
                classdict['data'] = yaml.load(file)
        except Exception:
            print "cannot load config file"
        return type.__new__(cls, classname, bases, classdict)


class ConfigLoader(object):
    __metaclass__ = Meta
    CONFIG_PATH = './config.yml'


if __name__ == '__main__':
    print ConfigLoader.data
