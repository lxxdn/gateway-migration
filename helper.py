#!/usr/bin/env python
# coding=utf-8

from config import ConfigLoader
import os


BLUEPRINT_PREFIX = os.path.join(
    ConfigLoader.data['gateway']['root'],
    ConfigLoader.data['gateway']['name'],
    'blueprints')


def write_to_init_file(m_name, content):
    init_file_path = os.path.join(
        BLUEPRINT_PREFIX, m_name, '__init__.py')
    __write_to_file(init_file_path, content)


def __write_to_file(f_dest, content):
    print "### f_dest: ", f_dest
    with open(f_dest, 'a+') as file:
        file.write(content)
