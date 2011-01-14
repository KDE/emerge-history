#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010, Intevation GmbH
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Intevation GmbH nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""Tool to generate Graphviz DOT file of the package dependencies
   for a given emerge package. Doubles as a library for explict
   dependency graph traverals.

   Usage:

   Precondition: Set the environment variables needed by emerge.

   $ python bin/dependencies.py -t <type of output> <emerge package> > deps.dot

   with <type of output> being the kind of output send to stdout.
   Possible values: 'dot', 'kwi' and 'xml'. Defaults to 'dot'

   The output is send to stdout. Piped into a file you may use
   dot to generate a graphical version.

   $ dot -T svg -o deps.svg deps.dot
"""

__author__  = "Sascha L. Teichmann <sascha.teichmann@intevation.de>"
__license__ = "New-style BSD"

import portage
import sys
import os
import utils
import graphviz
from argparse import ArgumentParser
from string import Template

OUTPUT_DOT = 0
OUTPUT_XML = 1
OUTPUT_KWI = 2

class Visitor(object):
    """Visitor applied to a node in the
       dependency graph during traversal
    """

    CONTINUE_CHILDREN = 1
    IGNORE_CHILDREN   = 2

    def beforeChildren(self, dummyNode, dummyContext):
        """Called before the children of the node are visited."""
        return Visitor.CONTINUE_CHILDREN

    def afterChildren(self, dummyNode, dummyContext):
        """Called after the children  of the node are visited."""
        return Visitor.CONTINUE_CHILDREN

def nlSeparated(node):
    """Replace ':' by newlines to make target look better in dot output."""
    return str(node).replace(":", r"\n")

class GraphvizCreator(Visitor):
    """Visitor to create DOT files from dependency graphs."""

    def afterChildren(self, node, context):
        visited, out, ranks = context
        if not node.children:
            max_depth = 666
        else:
            max_depth = node.maxDepth()
        ranks.setdefault(max_depth, set()).add(node)
        for child in node.children:
            link = '"%s" -> "%s"' % (
                nlSeparated(node), nlSeparated(child))
            if link not in visited:
                visited.add(link)
                out.append(link)
        return Visitor.CONTINUE_CHILDREN

    def createOutput(self, tree):
        visited = set()
        out = [
            'digraph "dependencies" {',
            'ranksep=2;',
            'size="6,6";' ]
        ranks = {}
        tree.visit(self, (visited, out, ranks))

        for v in ranks.itervalues():
            out.append("{ rank=same; ")
            for n in v:
                out.append('"%s";' % nlSeparated(n))
            out.append("}")

        out.append("}")

        return "\n".join(out)

class XMLCreator(Visitor):
    """Visitor to create an XML representation of the dependency graph."""

    def __init__(self):
        self.nodes_so_far = {}
        self.ignored      = False

    def beforeChildren(self, node, out):
        if not isinstance(node, DependenciesNode):
            return Visitor.CONTINUE_CHILDREN
        node_name = str(node)
        node_id = self.nodes_so_far.get(node_name)
        if node_id is not None:
            out.append('<dep ref="n%d"/>' % node_id)
            self.ignored = True
            return Visitor.IGNORE_CHILDREN

        new_id = len(self.nodes_so_far)

        self.nodes_so_far[node_name] = new_id
        out.append('<dep id="n%d" cat="%s" pgk="%s" ver="%s" tag="%s"'% (
            new_id,
            node.category, node.package, node.version, node.tag))
        if hasattr(node, "children") and not node.children:
            out.append("/>")
            self.ignored = True
            return Visitor.IGNORE_CHILDREN
        out.append(">")
        return Visitor.CONTINUE_CHILDREN

    def afterChildren(self, dummyNode, out):
        if self.ignored:
            self.ignored = False
        else:
            out.append("</dep>")
        return Visitor.CONTINUE_CHILDREN

    def createOutput(self, tree):
        out = ['<?xml version="1.0" encoding="UTF-8" ?>\n']
        out.append("<deps>")
        tree.visit(self, out)
        out.append("</deps>")
        return ''.join(out)

class KDEWinCreator( Visitor ):
    """ A visitor to generate a kdewin-installer config file """
    compiler = "vc90"
    mode = "deps"
    cats = dict()
    cats["data"] = []
    cats["KDE"] = []
    cats["kdesupport"] = []
    cats["win32libs"] = []

    def collectMetaData( self, node, context ):
        visited = context[0]
        if str( node ) not in visited:
            visited.add( str( node ) )
            metaData = node.metaData
            packageName = node.package
            if node.category == "virtual":
                return None
            if packageName.endswith( "-src" ) or packageName.endswith( "-pkg" ):
                packageName = packageName[ : -4 ]
            if "shortDescription" in metaData:
                if metaData["withCompiler"]:
                    asterisk = "-*"
                else:
                    asterisk = ""
                return "@pkgnotes " + packageName + asterisk + " " + metaData[ "shortDescription" ]
        return None

    def collectPackagesForCategory( self, node, context ):
        visited = context[0]
        if str( node ) not in visited:
            visited.add( str( node ) )
            if node.category in [ "kdesupport", "libs" ] and node not in self.cats[ "kdesupport" ]:
                self.cats[ "kdesupport" ].append( node )
                return None
            elif node.category.startswith( "kde" ) and node.category != "kdesupport" or node.category in [ "extragear", "kdeapps" ] and node not in self.cats[ "KDE" ]:
                self.cats[ "KDE" ].append( node )
                return None
            elif node.category == "data" and node not in self.cats[ "data" ]:
                self.cats[ "data" ].append( node )
                return None
            elif node.category in [ "testing", "win32libs-sources", "win32libs-bin" ] and node not in self.cats[ "win32libs" ]:
                self.cats[ "win32libs" ].append( node )
                return None
        return None

    def __getNodeDependencies( self, node ):
        if node.metaData["withCompiler"]:
            depString = " runtime-" + self.compiler
        else:
            depString = ""
        for child in node.children:
            childName = child.package
            if child.category == "virtual":
                depString += self.__getNodeDependencies( child )
            else:
                if childName.endswith( "-src" ) or childName.endswith( "-pkg" ):
                    childName = childName[ :-4 ]
                depString += " " + childName
                if child.metaData["withCompiler"]:
                    depString += "-" + self.compiler
        return depString

    def writeDependencyLine( self, node, context ):
        visited = context[0]
        packageName = node.package
        packageCategory = node.category
        if packageCategory == "virtual":
            return None
        if packageName.endswith( "-src" ) or packageName.endswith( "-pkg" ):
            packageName = packageName[ : -4 ]
        if "win32libs" in packageCategory:
            packageCategory = "win32libs"

        depString = "@deps " + packageName
        if node.metaData["withCompiler"]:
            depString += "-" + self.compiler
        deps = self.__getNodeDependencies( node )
        depString += deps
        if str( node ) not in visited: # and len( node.children ) > 0: # since runtime packages are not included, use a hack here
            visited.add( str( node ) )
            if len(deps) == 0:
                return None
            if not node.metaData["withCompiler"] and not node.dependencyVisited:
                node.dependencyVisited = True
                return depString
            elif not node.metaData["withCompiler"]:
                return None
            return depString
        return None

    def afterChildren( self, node, context ):
        out = context[1]

        if self.mode == "deps":
            result = self.writeDependencyLine( node, context )
        elif self.mode == "cats":
            result = self.collectPackagesForCategory( node, context )
        elif self.mode == "meta":
            result = self.collectMetaData( node, context )
        if result:
            out.append( result )
        return Visitor.CONTINUE_CHILDREN

    def __dumpCategories( self, out ):
        out.append( "; to which category packages belong to" )
        for _cat in self.cats:
            _str = "@categorypackages " + _cat
            num = 0
            for _node in self.cats[ _cat ]:
                _packageName = _node.package
                if _packageName.endswith( "-src" ) or _packageName.endswith( "-pkg" ):
                    _packageName = _packageName[:-4]
                if _node.metaData["withCompiler"]:
                    _str += " " + _packageName + "-" + self.compiler
                    num += 1
                else:
                    if not _node.categoryVisited:
                        _node.categoryVisited = True
                        _str += " " + _packageName
                        num += 1
                if num > 10:
                    num = 0
                    out.append( _str )
                    _str = "@categorypackages " + _cat
            if num > 0:
                out.append( _str )
        out.append( ";" )

    def createOutput( self, tree ):
        out = []

        template = Template( file( os.path.join( os.path.dirname( sys.argv[ 0 ] ), "config.txt.template" ) ).read() )

        visited = set()
        ranks = {}
        self.mode = "cats"
        for self.compiler in [ "x86-mingw4", "mingw4", "vc90", "vc100" ]:
            visited = set()
            tree.visit( self, ( visited, out, ranks ) )
            self.__dumpCategories( out )
        _cat = "\n".join( out )
        out = []
        self.mode = "deps"
        for self.compiler in [ "x86-mingw4", "mingw4", "vc90", "vc100" ]:
            visited = set()
            out.append( "; package dependencies for compiler " + self.compiler )
            tree.visit( self, ( visited, out, ranks ) )
            out.append( ";" )

        _dep = "\n".join( out )
        out = []
        visited = set()
        ranks = {}
        self.mode = "meta"
        tree.visit( self, ( visited, out, ranks ) )
        _meta = "\n".join( out )
        return template.safe_substitute( { 'categorypackages': _cat, 'dependencies': _dep, 'pkgnotes': _meta } )

class DependenciesNode(object):
    """A node in the dependency graph."""

    def __init__(self, category, package, version, tag = "1", children = None):
        if children is None:
            children = []
        self.category = category
        self.package  = package
        self.version  = version
        self.tag      = tag
        self.children = children
        self.parents  = []
        self.metaData = dict()
        self.categoryVisited = False
        self.dependencyVisited = False

    def __str__(self):
        return "%s:%s:%s:%s" % (
            self.category, self.package, self.version, self.tag)

    def visit(self, visitor, context):
        """Apply a visitor to this node."""
        if visitor.beforeChildren(self, context) == Visitor.CONTINUE_CHILDREN:
            for child in self.children:
                child.visit(visitor, context)
        visitor.afterChildren(self, context)

    def maxDepth(self):
        """Calculates the maximum depth of this node."""
        if not self.parents:
            return 0
        pdepth = -1
        for p in self.parents:
            d = p.maxDepth()
            if d > pdepth:
                pdepth = d
        # TODO: use something like max(x.maxDepth() for x in self.parents)
        return pdepth + 1

class DependenciesTree(object):
    """A dependency tree. More a kind of DAG (directed acyclic graph)."""

    def __init__(self):
        self.roots    = []
        self.key2node = {}

    def addDependencies(self, category, package, version = "", dep_type="both"):
        """Add a new root dependency tree to this graph."""

        pi = portage.PortageInstance

        if portage.emergePlatform.isCrossCompilingEnabled() \
        or utils.isSourceOnly():
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
            tag = pi.getDefaultTarget( category, package, version )
        except:
            tag = "1"

        node = self.buildDepNode( category, package, version, tag, dep_type )

        if not node in self.roots:
            self.roots.append(node)

    def buildDepNode(self, category, package, version, tag, dep_type="both"):
        """Recursive method to construct the nodes of the dependency tree."""

        pi = portage.PortageInstance

        if portage.emergePlatform.isCrossCompilingEnabled() \
        or utils.isSourceOnly():
            sp = pi.getCorrespondingSourcePackage(package)
            if sp:
                # we found such a package and we're allowed to replace it
                category = sp[0]
                package = sp[1]
                version = pi.getNewestVersion(category, package)

        try:
            tag = pi.getDefaultTarget( category, package, version )
        except:
            tag = "1"

        key = "%s-%s-%s-%s" % (category, package, version, tag)
        try:
            node = self.key2node[key]
            return node
        except KeyError:
            pass

        children = []

        for t in portage.getDependencies(category, package, version, (dep_type=="runtime")):
            sub_node = self.buildDepNode(t[0], t[1], t[2], tag, dep_type)
            children.append(sub_node)
        node = DependenciesNode(category, package, version, tag, children)
        node.metaData = pi.getMetaData(category, package, version)

        for child in children:
            child.parents.append(node)

        self.key2node[key] = node

        return node

    def visit(self, visitor, context):
        """Apply a visitor to all parts of this graph."""
        for root in self.roots:
            root.visit(visitor, context)

def parseOptions():
    usage = "%(prog)s [options] CATEGORY/PACKAGE\n" \
            "   or: %(prog)s -f packagelist.txt [packagelist2.txt ...]\n" \
            "   or: %(prog)s --file=packagelist.txt \n"
    parser = ArgumentParser(prog=sys.argv[0], usage=usage)

    parser.add_argument("-t", "--type", action = "store", default = OUTPUT_DOT,
            help=("Change the output format type "
                  "possible values: xml kwi, dot"))
    parser.add_argument("-f", "--file", dest = "filenames", metavar = "FILENAME",
            help="add a filename for a packageList ", nargs='+', required=True)
    parser.add_argument("-o", "--output", dest = "outputname", metavar = "FILENAME",
            help=" ")
    parser.add_argument("-d", "--depstyle", action = "store", default = "both",
            help="possible values: both, runtime")

    args = parser.parse_args()
    if not (hasattr(args, "filenames") and not args.filenames == None):
        if len(args) < 1:
            parser.error("Incorrect number of arguments")
            sys.exit(1)
        if len(args[0].split("/")) != 2:
            parser.error("Not a valid Category/Package name")
            sys.exit(1)
    return args

def parsePackageListFiles( filenames ):
    depList = []
    for filename in filenames:
        packagefile = file( filename )
        for line in packagefile:
            if not line.startswith( '#' ):
                cat, pac, target, patchlvl = line.strip().split( ',' )
                if pac.endswith( "-src" ):
                    cat, pac = portage.PortageInstance.getCorrespondingBinaryPackage(pac)
                depList.append( ( cat, pac, target, patchlvl ) )
        packagefile.close()
    return depList

def main():

    args = parseOptions()
    if args.type == "xml":
        output_type = OUTPUT_XML
    elif args.type == "kwi":
        output_type = OUTPUT_KWI
    else:
        output_type = OUTPUT_DOT

    depstyle = args.depstyle
    if not args.depstyle in ['both', 'runtime']:
        depstyle = "both"
    output = ""
    if hasattr(args, "filenames") and args.filenames != None:
        packageList = parsePackageListFiles( args.filenames )
        output = dumpDependenciesForPackageList(packageList, output_type, depstyle)
    else:
        output = dumpDependencies(args[0], output_type, depstyle)

    if hasattr(args, "outputname") and args.outputname:
        print "writing file ", args.outputname, os.path.dirname( args.outputname )
        if os.path.dirname( args.outputname ) and not os.path.exists( os.path.dirname( args.outputname ) ):
            os.makedirs( os.path.dirname( args.outputname ) )
        f = open( args.outputname, "w" )
        f.write( output )
        f.close()

        if output_type == OUTPUT_DOT:
            _graphviz = graphviz.GraphViz()

            if not _graphviz.runDot( args.outputname, args.outputname + '.pdf', 'pdf' ):
                exit( 1 )

# we don't want to open the output automatically, at least not always
#        _graphviz.openOutput()
    else:
        print output

def createOutput(output_type, dep_tree):
    """return output for output_type"""
    if  output_type == OUTPUT_XML:
        creator = XMLCreator()
    elif output_type == OUTPUT_DOT:
        creator = GraphvizCreator()
    elif output_type == OUTPUT_KWI:
        creator = KDEWinCreator()
    else:
        assert False, 'unknown output_type %d' % output_type

    return creator.createOutput(dep_tree)

def dumpDependencies(category, output_type=OUTPUT_DOT, dep_type="both"):
    # little workaround to not display debug infos in generated output
    # TODO: define a context function and use this here and in the next function
    # with Verbosity(0):
    #     generate dep_tree
    old_emerge_verbose = os.environ.get('EMERGE_VERBOSE')
    utils.setVerbose( 0 )

    packageList, categoryList = portage.getPackagesCategories(category)
    dep_tree = DependenciesTree()

    for _category, _package in zip(categoryList, packageList):
        dep_tree.addDependencies(_category, _package, dep_type=dep_type)

    if old_emerge_verbose is not None:
        os.environ['EMERGE_VERBOSE'] = old_emerge_verbose

    return createOutput(output_type, dep_tree)

def dumpDependenciesForPackageList(packageList, output_type=OUTPUT_DOT, dep_type="both"):
    # little workaround to not display debug infos in generated output
    old_emerge_verbose = os.environ.get('EMERGE_VERBOSE')
    utils.setVerbose( 0 )

    dep_tree = DependenciesTree()

    for category, package, dummyTarget, dummyPatchlevel in packageList:
        dep_tree.addDependencies(category, package, dep_type=dep_type)

    if old_emerge_verbose is not None:
        os.environ['EMERGE_VERBOSE'] = old_emerge_verbose

    return createOutput(output_type, dep_tree)

if __name__ == '__main__':
    main()
