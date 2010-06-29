#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# copyright 2010 by Intevation GmbH

__author__  = "Sascha L. Teichmann <sascha.teichmann@intevation.de>"
__license__ = "GNU General Public License (GPL)"

import portage
import utils
import sys
import os

class DependenciesNode(object):

    def __init__(self, category, package, version, tag = "1", children = None):
        if children is None: children = []
        self.category = category
        self.package  = package
        self.version  = version
        self.tag      = tag
        self.children = children
        self.parents  = []

    def __str__(self):
        return "%s:%s:%s:%s" % (
            self.category, self.package, self.version, self.tag)

    def visit(self, visitor, context):
        for child in self.children:
            child.visit(visitor, context)
        visitor(self, context)

    def max_depth(self):
        if not self.parents:
            return 0
        pdepth = -1
        for p in self.parents:
            d = p.max_depth()
            if d > pdepth: pdepth = d
        return pdepth + 1

class DependenciesTree(object):

    def __init__(self):
        self.roots    = []
        self.key2node = {}

    def add_dependencies(self, category, package, version = ""):

        pi = portage.PortageInstance

        if portage.platform.isCrossCompilingEnabled() \
        or os.getenv("EMERGE_SOURCEONLY") == "True" or os.getenv("EMERGE_SOURCEONLY") == "1":
            sp = pi.getCorrespondingSourcePackage(package)
            if sp:
                # we found such a package and we're allowed to replace it
                category = sp[0]
                package = sp[1]
                version = pi.getNewestVersion(category, package)

        if category == "":
            category = pi.getCategory(package)

        if version == "":
            version = pi.getNewestVersion(category, package)

        try:
            tag = pi.getAllTargets(category, package, version ).keys()[0]
        except:
            tag = "1"

        node = self.build_dep_node(category, package, version, tag)

        if not node in self.roots:
            self.roots.append(node)

    def build_dep_node(self, category, package, version, tag):
        key = "%s-%s-%s-%s" % (category, package, version, tag)
        try:
            node = self.key2node[key]
            #print >> sys.stderr, "found node for key '%s'" % key
            return node
        except KeyError:
            #print >> sys.stderr, "Node for '%s' not found" % key
            pass

        children = []

        for t in portage.getDependencies(category, package, version):
            sub_node = self.build_dep_node(t[0], t[1], t[2], tag)
            children.append(sub_node)

        node = DependenciesNode(category, package, version, tag, children)
        for child in children:
            child.parents.append(node)

        self.key2node[key] = node

        return node

    def visit(self, visitor, context):
        for root in self.roots:
            root.visit(visitor, context)

    def as_graphviz(self):
        def visitor(node, context):
            visited, out, ranks = context
            if not node.children: max_depth = 666
            else:                 max_depth = node.max_depth()
            ranks.setdefault(max_depth, set()).add(node)
            for child in node.children:
                link = '"%s" -> "%s"' % (node, child)
                if link not in visited:
                    visited.add(link)
                    out.append(link)
        visited = set()
        out = [
            'digraph "dependencies" {', 
            'ranksep=2;',
            'size="6,6";' ]
        ranks = {}
        self.visit(visitor, (visited, out, ranks))

        for k, v in ranks.iteritems():
            out.append("{ rank=same; ")
            for n in v: out.append('"%s";' % n)
            out.append("}")

        out.append("}")

        return "\n".join(out)

def main():
    if len(sys.argv) < 2:
        print >> sys.stderr, "missing package"
        sys.exit(1)

    packageList, categoryList = portage.get_packages_categories(sys.argv[1])

    dep_tree = DependenciesTree()

    for catagory, package in zip(categoryList, packageList):
        dep_tree.add_dependencies(catagory, package)

    print dep_tree.as_graphviz()

if __name__ == '__main__':
    main()
