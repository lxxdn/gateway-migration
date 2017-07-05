#!/usr/bin/env python
# coding=utf-8

from config import ConfigLoader
from ast_factory import AstFilterFactory
import os
import ast

def __find_ctlr_name_source(ctlr_name):
    """
    Return value is the class definition of the controller class
    """

    legacy_fulishe_root = ConfigLoader.data['fulishe-legace']['root']
    for root, _, files in os.walk(legacy_fulishe_root):
        for f_name in files:
            if not f_name.endswith('.py'):
                continue

            with open(os.path.join(root, f_name)) as file:
                content = file.read()
                clazz = AstFilterFactory('ClassDef', [lambda node: node.name == ctlr_name])
                visitor = clazz()
                visitor.visit(ast.parse(content))
                if visitor.nodes:
                    return visitor.nodes[0]

    return None


def __filter_useles_func(class_def_node):
    """
    Filter the functions that are not used any place.
    """
    visitor = AstFilterFactory('FunctionDef')()
    visitor.visit(class_def_node)
    func_nodes = visitor.nodes



def __convert_func(func_nodes):
    return __to_jsonresponse(func_nodes)


def __to_jsonresponse(func_nodes):
    pass


def gen_controller():
    pass
