#!/usr/bin/env python
# coding=utf-8

import ast


def create_ast_collector_visitor_class(visitor_type, conditions=None):
    """
    This function aims to create a class to find all the node whose type is visitor_type
    and matches all the conditions
    """

    def general_visitor(self, node):
        global conditions

        if not conditions:
            conditions = [lambda n: True]
        if reduce((lambda x, y: x and y), [cond(node) for cond in conditions]):
            self.nodes.append(node)
        ast.NodeVisitor.generic_visit(self, node)

    classdict = {}
    classdict['nodes'] = []
    classdict['visit_' + visitor_type] = general_visitor
    return type("AstVisitor", (ast.NodeVisitor, ), classdict)


AstFilterFactory = create_ast_collector_visitor_class
