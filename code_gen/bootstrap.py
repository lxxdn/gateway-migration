#!/usr/bin/env python
# coding=utf-8
import os
from config import ConfigLoader


def gen_scaffold(module_name):
    """
    This function will create the basic new module file structure
    gateway_root/name/blueprints/new_module/__init__.py
    gateway_root/name/blueprints/new_module/views.py
    gateway_root/name/blueprints/new_module/schemas.py
    """
    gateway_module_root = os.path.join(
        ConfigLoader.data['gateway']['root'],
        ConfigLoader.data['gateway']['name'],
        'blueprints',
        module_name)

    if not os.path.exists(gateway_module_root):
        os.makedirs(gateway_module_root)

    for f_name in ['__init__.py', 'views.py', 'schemas.py']:
        with open(os.path.join(gateway_module_root, f_name), 'w+') as f:
            f.write('# coding=utf-8\n')
