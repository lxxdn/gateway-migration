#!/usr/bin/env python
# coding=utf-8
import sys
from code_gen.bootstrap import gen_scaffold
from code_gen.routes import gen_routes
from code_gen.controller import gen_controller
import helper


def main():
    f_controller_name = sys.argv[1]
    g_module_name = sys.argv[2]

    gen_scaffold(g_module_name)

    route_code = gen_routes(f_controller_name, g_module_name)
    helper.write_to_init_file(g_module_name, route_code)

    gen_controller(f_controller_name)


def write_to_file(f_dest, content):
    with open(f_dest, 'a+') as f:
        f.write(content)


if __name__ == '__main__':
    main()
