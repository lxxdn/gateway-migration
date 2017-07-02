#!/usr/bin/env python
# coding=utf-8

import ast
from ast_factory import AstFilterFactory


def find_call_with_patterns(content, patterns):
    """
    pattern is a dict which describes the ast object structure
    """
    clazz = AstFilterFactory('Call', patterns)
    visitor = clazz()
    visitor.visit(ast.parse(content))
    return visitor.nodes
