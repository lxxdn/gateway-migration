#!/usr/bin/env python
# coding=utf-8

from config import ConfigLoader
from ast_helpers import find_call_with_patterns
import os
import ast
from code_gen import SEGMENT_SEPERATOR
import codegen
import autopep8
from context import current_ctx


def gen_routes(legacy_controller_name, new_module_name):
    nodes = __get_routes_from_origin(legacy_controller_name)
    nodes = __convert_to_gateway_routes(
        nodes, legacy_controller_name, new_module_name)

    route_helpers = set([node.func.id for node in nodes])
    route_code = []

    route_code.append("from flask import Blueprint")
    route_code.append("from ..routes import " + ', '.join(route_helpers))
    route_code.append('import views')
    route_code.append(SEGMENT_SEPERATOR)
    route_code.append(
        "{0} = Blueprint('{0}', __name__)".format(new_module_name))
    route_code.append(SEGMENT_SEPERATOR)
    route_code.append(__gen_routes_code(nodes))

    return autopep8.fix_code("\n".join(route_code))


def __get_route_info_from_node(node):
    endpoint = None
    route_name = node.func.id
    url = node.args[0].s
    for kw in node.keywords:
        if kw.arg == 'method':
            method = kw.value.s
        elif kw.arg == 'name':
            endpoint = kw.value.s
        elif kw.arg == 'callback':
            ctlr_action = kw.value.attr

    return route_name, url, method, endpoint, ctlr_action


def __get_routes_from_origin(legacy_controller_name):
    nodes = []
    routes_location = os.path.join(
        ConfigLoader.data['fulishe-legacy']['root'], 'front_main2/route')

    for root, _, files in os.walk(routes_location):
        for f in files:
            if not f.endswith('.py'):
                continue
            with open(os.path.join(root, f)) as file:
                content = file.read()
                nodes += find_call_with_patterns(content,
                                                 __routes_node_conditions(legacy_controller_name))

    return nodes


def __routes_node_conditions(legacy_controller_name):
    conditions = []

    "find the routes which are related to the legacy controlelr name"
    def cond(node):
        if not hasattr(node, 'keywords'):
            return False
        nodes = filter(
            lambda node: node.arg == 'callback' and hasattr(node.value, 'value') and hasattr(
                node.value.value, 'id') and
            node.value.value.id == legacy_controller_name,
            node.keywords)

        return len(nodes) != 0

    conditions.append(cond)

    return conditions


def __convert_to_gateway_routes(nodes, ctlr_name, m_name):
    result = []
    route_helper_map = ConfigLoader.data['gateway']['route_helper_map']
    for node in nodes:
        route_name, url, method, endpoint, ctlr_action = __get_route_info_from_node(
            node)

        # this data will be used later
        route_methods = current_ctx.get('route_methods') or set()
        route_methods.add(ctlr_action)
        current_ctx.set('route_methods', route_methods)

        if route_name in route_helper_map.keys():
            n = ast.Call(func=ast.Name(id=route_helper_map[route_name], ctx=ast.Load()), args=[ast.Name(id=m_name, ctx=ast.Load()), ast.Str(s=url), ast.Attribute(value=ast.Attribute(value=ast.Name(id='views', ctx=ast.Load(
            )), attr=ctlr_name, ctx=ast.Load()), attr=ctlr_action, ctx=ast.Load())], keywords=[ast.keyword(arg='method', value=ast.Str(s=method)), ast.keyword(arg='endpoint', value=ast.Str(s=endpoint))], starargs=None, kwargs=None)

            result.append(n)

    return result


def __gen_routes_code(nodes):
    return '\n'.join([codegen.to_source(n) for n in nodes])


def main():
    gen_routes('SaleDataAPIController')


if __name__ == '__main__':
    main()
