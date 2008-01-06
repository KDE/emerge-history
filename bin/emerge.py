# this will emerge some programs...

# call this with "emerge.py <packageName> <action>"
# where packageName is the program you want to install
# and action is the action you want to do, see base.py
#
# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>

# syntax:
# emerge <options> <action> <packageName>
#
# action can be:
# --fetch, --unpack, --compile, --install, --qmerge
#
# options can be:
# -p for pretend

import sys
import os
import utils

def usage():
    print
    print 'usage: emerge [-f|-p|-q|-v|--offline][--fetch|--unpack|--compile|--install|'
    print '                            --manifest|--qmerge|--unmerge|--package|'
    print '                            --full-package] packageName'
    print 'emerge.py is a script for easier building.'
    print
    print 'flags:'
    print '-p               pretend to do everything - a dry run'
    print '-q               suppress all output'
    print '-f               force removal of files with unmerge'
    print '-v               print additional output (increase the verbosity level)'
    print '--offline        don\'t try to download anything'
    print '--buildtype=[KdeBuildType] where KdeBuildType is one of the used BuildTypes'
    print '                 This will automatically overrun all buildtype definitions'
    print '                 made in the package\'s .py-file'
    print 'options:'
    print '--fetch          just fetch the packages'
    print '--unpack         unpack the packages and apply the patches if needed'
    print '--compile        configure and build the package'
    print '--install        install the package to an image directory'
    print '--manifest       add the installdb files to the image directory'
    print '--qmerge         install the image directories contents to the kderoot'
    print '--package        package the image directory with the kdewin-packager[*]'
    print '--full-package   make all of the above steps'
    print '--unmerge        try to unmerge package'
    print
    print '[*] - this requires the packager to be installed already'
    print 'please see http://windows.kde.org for more information'
    print 'send bugs and feature requests to kde-windows@kde.org'
    print

def doExec( category, package, version, action, opts ):
    if utils.verbose() > 2:
        print "emerge doExec called opts:", opts
    file = os.path.join( utils.getPortageDir(), category, package, "%s-%s.py" % \
                         ( package, version ) )
    opts_string = ( "%s " * len( opts ) ) % tuple( opts )
    commandstring = "python %s %s %s" % ( file, action, opts_string )
    if utils.verbose() > 1:
        print "file:", file
        print "commandstring", commandstring
    utils.system( commandstring ) or utils.die( "running %s" % commandstring )
    return True

def handlePackage( category, package, version, buildAction, opts ):
    if utils.verbose() > 1:
        print "emerge handlePackage called:", category, package, version, buildAction
    if ( buildAction == "all" or buildAction == "full-package" ):
        success = doExec( category, package, version, "fetch", opts )
        success = success and doExec( category, package, version, "unpack", opts )
        success = success and doExec( category, package, version, "compile", opts )
        success = success and doExec( category, package, version, "cleanimage", opts )
        success = success and doExec( category, package, version, "install", opts )
        if ( buildAction == "all" ):
            success = success and doExec( category, package, version, "manifest", opts )
        if ( buildAction == "all" ):
            success = success and doExec( category, package, version, "qmerge", opts )
        if( buildAction == "full-package" ):
            success = success and doExec( category, package, version, "package", opts )

    elif ( buildAction in ["fetch", "unpack", "compile", "configure", "make", "qmerge", "package", "manifest", "unmerge"] ):
        success = doExec( category, package, version, buildAction, opts )
    elif ( buildAction == "install" ):
        success = doExec( category, package, version, "cleanimage", opts )
        success = success and doExec( category, package, version, "install", opts )
    elif ( buildAction == "version-dir" ):
        print "%s-%s" % ( package, version )
        success = True
    elif ( buildAction == "version-package" ):
        print "%s-%s-%s" % ( package, os.getenv( "KDECOMPILER" ), version )
        success = True
    else:
        success = utils.error( "could not understand this buildAction: %s" % buildAction )

    return success

buildAction = "all"
packageName = None
doPretend = False
stayQuiet = False
buildTests = False
offline = False
opts = ""

if len( sys.argv ) < 2:
    usage()
    exit( 1 )

ncopy=os.getenv( "EMERGE_NOCOPY" )
if ( ncopy == "True" ):
    nocopy = True
else:
    nocopy = False

bTests=os.getenv( "EMERGE_BUILDTESTS" )
if ( bTests == "True" ):
    buildTests = True
else:
    buildTests = False

verb = os.getenv( "EMERGE_VERBOSE" )
if verb == None or not verb.isdigit():
    verbose = 1
    os.environ["EMERGE_VERBOSE"] = str( verbose )
else:
    verbose = int( verb )
    
opts = list()

executableName = sys.argv.pop( 0 )
for i in sys.argv:
    if ( i == "-p" ):
        doPretend = True
    elif ( i == "-q" ):
        stayQuiet = True
    elif ( i == "-t" ):
        buildTests = True
        os.environ["EMERGE_BUILDTESTS"] = "True"
    elif ( i == "--offline" ):
        opts.append( "--offline" )
        offline = True
        os.environ["EMERGE_OFFLINE"] = "True"
    elif ( i == "-f" ):
        opts.append( "--forced" )
    elif ( i.startswith( "--version=" ) ):
        srcversion = i.replace( "--version=", "" )
    elif ( i.startswith( "--buildtype=" ) ):
        os.environ["EMERGE_BUILDTYPE"] = i.replace( "--buildtype=", "" )
    elif ( i == "-v" ):
        verbose = verbose + 1
        os.environ["EMERGE_VERBOSE"] = str( verbose )
    elif ( i == "--nocopy" ):
        nocopy = True
        os.environ["EMERGE_NOCOPY"] = str( nocopy )
    elif ( i == "--version-dir" ):
        buildAction = "version-dir"
        stayQuiet = True
    elif ( i == "--version-package" ):
        buildAction = "version-package"
        stayQuiet = True
    elif ( i in ["--fetch", "--unpack", "--compile", "--configure", "--make",
                 "--install", "--qmerge", "--manifest", "--package", "--unmerge",
                 "--full-package"] ):
        buildAction = i[2:]
    elif ( i.startswith( "-" ) ):
        usage()
        exit ( 1 )
    else:
        packageName = i
if stayQuiet == True:
    verbose = 0
    os.environ["EMERGE_VERBOSE"]=str( verbose )

# get KDEROOT from env
KDEROOT = os.getenv( "KDEROOT" )

if utils.verbose() >= 1:
    print "buildAction:", buildAction
    print "doPretend:", doPretend
    print "packageName:", packageName
    print "buildType:", os.getenv( "EMERGE_BUILDTYPE" )
    print "buildTests:", os.getenv( "EMERGE_BUILDTESTS" )
    print "verbose:", os.getenv( "EMERGE_VERBOSE" )
    print "KDEROOT:", KDEROOT
    

# adding emerge/bin to find base.py and gnuwin32.py etc.
os.environ["PYTHONPATH"] = os.getenv( "PYTHONPATH" ) + ";" + os.path.join( os.getcwd(), os.path.dirname( executableName ) )

deplist = []
utils.solveDependencies( "", packageName, "", deplist )
if utils.verbose() > 2:
    print "deplist:", deplist

deplist.reverse()
success = True

if ( buildAction != "all" ):
    """if a buildAction is given, then do not try to build dependencies"""
    """and do the action although the package might already be installed"""
    package = deplist[-1]
    ok = handlePackage( package[0], package[1], package[2], buildAction, opts )
else:
  for package in deplist:
    file = os.path.join( KDEROOT, "emerge", "portage", package[0], package[1], "%s-%s.py" % ( package[1], package[2] ) )
    if ( doPretend ):
        if ( utils.isInstalled( package[0], package[1], package[2] ) ):
            if utils.verbose() > 1 and package[1] == packageName:
                print "already installed %s/%s-%s" % ( package[0], package[1], package[2] )
            elif utils.verbose() > 2 and not package[1] == packageName:
                print "already installed %s/%s-%s" % ( package[0], package[1], package[2] )
        else:
            if utils.verbose() > 0:
                print "pretending %s/%s-%s" % ( package[0], package[1], package[2] )
    else:
        if ( not utils.isInstalled( package[0], package[1], package[2] ) ):
            ok = handlePackage( package[0], package[1], package[2], buildAction, opts )
            if ( not ok ):
                print "fatal error: package %s/%s-%s %s failed" % \
                    (package[0], package[1], package[2], buildAction)
        else:
            if utils.verbose() > 1 and package[1] == packageName:
                print "already installed %s/%s-%s" % ( package[0], package[1], package[2] )
            elif utils.verbose() > 2 and not package[1] == packageName:
                print "already installed %s/%s-%s" % ( package[0], package[1], package[2] )
