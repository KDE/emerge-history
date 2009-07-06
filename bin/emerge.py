# -*- coding: utf-8 -*-
# this will emerge some programs...

# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>

import sys
import os
import utils

def usage():
    print """
Usage:
    emerge [[ command and flags ] [ singletarget ]
            [ command and flags ] [ singletarget ]
            ... ]

    where singletarget can be of the form:
        category
        package
        category/package

Emerge is a tool for building KDE-related software under Windows. emerge
automates it, looks for the dependencies and fetches them automatically.
Some options should be used with extreme caution since they will
make your kde installation unusable in 999 out of 1000 cases.

Commands (no packagename needed - will be ignored when given):

--print-installed               This will show a list of all packages that
                                are installed currently. It queries both
                                databases (etc\portage\installed) and the
                                manifest directory - it prints out only those
                                packages that are contained within
                                --print-installable
--print-installable             This will give you a list of packages that can
                                be installed. Currently you don't need to
                                enter the category and package: only the
                                package will be enough.
--update-all                    this option tries to update all installed 
                                packages that contain one or multiple svn 
                                targets. This is equivalent to running all
                                those packages with the flag --update.

Commands (must have a packagename):

--print-targets     This will print all the different targets 
                    one package can contain: different releases might have
                    different tags that are build as targets of a package. As
                    an example: You could build the latest amarok sources with
                    the target 'svnHEAD' the previous '1.80' release would be
                    contained as target '1.80'.

--fetch             for most non-KDE packages: retrieve package sources.
--unpack            for most non-KDE packages: unpack package sources and make
                    up the build directory.
                    for KDE packages: get package source from SVN and make up
                    the build directory.
--compile           compile the sources: this includes configure'ing/cmake'ing
                    and running [mingw32-|n|]make.
--configure         configure the sources (support is package specific)
--make              run [mingw32-|n|]make (support is package specific)
--install           This will run [mingw32-|n|]make install into the image 
                    directory of each package.
--manifest          This step creates the files contained in the manifest dir.
--qmerge            This will merge the image directory into the KDEROOT
--test              This will run the unittests if they are present
--package           This step will create a package out of the image directory
                    instead of merge'ing the image directory into the KDEROOT
                    (Requires the packager to be installed already.)
--full-package      This will create packages instead of installing stuff to
                    KDEROOT
--install-deps      This will fetch and install all required dependencies for 
                    the specified package
--unmerge           this uninstalls a package from KDEROOT - it requires a
                    working manifest directory. unmerge only delete unmodified 
                    files by default. You may use the -f or --force option to 
                    let unmerge delete all files unconditional.

Flags:

--buildtype=[BUILDTYPE]         This will override the build type set by the
                                environment option EMERGE_BUILDTYPE .
                                Please set it to one out of Release, Debug,
                                RelWithDebInfo, MinSizeRel
--target=[TARGET]               This will override the build of the default
                                target. The default Target is marked with a
                                star in the printout of --print-targets
--patchlevel=[PATCHLEVEL]       This will add a patch level when used together 
                                with --package                               

-i          ignore install: using this option will install a package over an
            existing install. This can be useful if you want to check some
            new code and your last build isn't that old. This option might
            cause some problems though: if you want to update Qt e.g. the
            building of qmake depends on the existance on the system - thus
            using -i will result in a wrong qt package (as has happened when
            updating from qt4.3 to qt4.4).
-p          probing: emerge will only look which files it has to build
            according to the list of installed files and according to the
            dependencies of the package.
-q          quiet: there should be no output - The verbose level should be 0
-t          test: if used on an KDE target it will override the environment
            variable and build the target with -DKDE_BUILD_TESTS=ON
-v          verbose: increases the verbose level of emerge.
            verbose level 1 contains some notes from emerge, all output of
            cmake, make and other programs that are used. verbose level 2
            adds an option VERBOSE=1 to make and emerge is more verbose
            highest level is verbose level 3.
--noclean   this option will try to use an existing build directory. Please
            handle this option with care - it will possibly break if the
            directory isn't existing.
--nocopy    this option is deprecated. In older releases emerge would have
            copied everything from the SVN source tree to a source directory
            under %KDEROOT%\\tmp - currently nocopy is applied by default if
            EMERGE_NOCOPY is not set to "False". Be aware that setting
            EMERGE_NOCOPY to "True" might slow down the build process,
            irritate you and increase the disk space roughly by the size of
            SVN source tree.
--offline   do not try to connect to the internet: KDE packages will try to
            use an existing source tree and other packages would try to use
            existing packages in the download directory. If that doesn't
            work, the build will fail.
--update    this option is the same as '-i --noclean'. It will update a single
            package that is already installed.

Internal options or options that aren't fully implemented yet:
PLEASE DO NOT USE!
--version-dir
--version-package

More information see the README or http://windows.kde.org/.
Send feedback to <kde-windows@kde.org>.

"""

def doExec( category, package, version, action, opts ):
    utils.debug( "emerge doExec called. action: %s opts: %s" % (action, opts), 2 )
    fileName = os.path.join( utils.getPortageDir(), category, package, "%s-%s.py" % \
                         ( package, version ) )
    opts_string = ( "%s " * len( opts ) ) % tuple( opts )
    commandstring = "python %s %s %s" % ( fileName, action, opts_string )

    utils.debug( "file: " + fileName, 1 )
    try:
        utils.system( commandstring ) or utils.die( "running %s" % commandstring )
    except:
        return False
    return True

def handlePackage( category, package, version, buildAction, opts ):
    utils.debug( "emerge handlePackage called: %s %s %s %s" % (category, package, version, buildAction), 2 )

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

    elif ( buildAction in [ "fetch", "unpack", "preconfigure", "configure", "compile", "make", "qmerge", "package", "manifest", "unmerge", "test" ] and category and package and version ):
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
    elif ( buildAction == "print-installable" ):
        utils.printInstallables()
        success = True
    elif ( buildAction == "print-installed" ):
        utils.printInstalled()
        success = True
    elif ( buildAction == "print-targets" ):
        utils.printTargets( category, package, version )
        success = True
    elif ( buildAction == "install-deps" ):
        success = True
    else:
        success = utils.error( "could not understand this buildAction: %s" % buildAction )

    return success

#
# "main" action starts here
#

buildAction = "all"
packageName = None
doPretend = False
stayQuiet = False
ignoreInstalled = False
updateAll = False
opts = ""
if len( sys.argv ) < 2:
    usage()
    utils.die("")

environ = dict()
environ["EMERGE_NOCOPY"]        = os.getenv( "EMERGE_NOCOPY" )
environ["EMERGE_NOUPDATE"]      = os.getenv( "EMERGE_NOUPDATE" )
environ["EMERGE_NOCLEAN"]       = os.getenv( "EMERGE_NOCLEAN" )
environ["EMERGE_VERBOSE"]       = os.getenv( "EMERGE_VERBOSE" )
environ["EMERGE_BUILDTESTS"]    = os.getenv( "EMERGE_BUILDTESTS" )
environ["EMERGE_OFFLINE"]       = os.getenv( "EMERGE_OFFLINE" )
environ["EMERGE_FORCED"]        = os.getenv( "EMERGE_FORCED" )
environ["EMERGE_VERSION"]       = os.getenv( "EMERGE_VERSION" )
environ["EMERGE_BUILDTYPE"]     = os.getenv( "EMERGE_BUILDTYPE" )
environ["EMERGE_TARGET"]        = os.getenv( "EMERGE_TARGET" )
environ["EMERGE_TARGET"]        = os.getenv( "EMERGE_PKGPATCHLVL" )

if ( environ['EMERGE_NOCOPY'] == "True" ):
    nocopy = True
else:
    nocopy = False

if ( environ['EMERGE_NOUPDATE'] == "True" ):
    noupdate = True
else:
    noupdate = False

if environ['EMERGE_VERBOSE'] == None or not environ['EMERGE_VERBOSE'].isdigit():
    verbose = 1
    os.environ["EMERGE_VERBOSE"] = str( verbose )
else:
    verbose = int( environ[ "EMERGE_VERBOSE" ] )
    
opts = list()

executableName = sys.argv.pop( 0 )
for i in sys.argv:
    if ( i == "-p" ):
        doPretend = True
    elif ( i == "-q" ):
        stayQuiet = True
    elif ( i == "-t" ):
        os.environ["EMERGE_BUILDTESTS"] = "True"
    elif ( i == "--offline" ):
        opts.append( "--offline" )
        os.environ["EMERGE_OFFLINE"] = "True"
    elif ( i == "-f" or i == "--force" ):
        os.environ["EMERGE_FORCED"] = "True"
    elif ( i.startswith( "--buildtype=" ) ):
        os.environ["EMERGE_BUILDTYPE"] = i.replace( "--buildtype=", "" )
    elif ( i.startswith( "--target=" ) ):
        os.environ["EMERGE_TARGET"] = i.replace( "--target=", "" )
    elif ( i.startswith( "--patchlevel=" ) ):
        os.environ["EMERGE_PKGPATCHLVL"] = i.replace( "--patchlevel=", "" )
    elif ( i == "-v" ):
        verbose = verbose + 1
        os.environ["EMERGE_VERBOSE"] = str( verbose )
    elif ( i == "--nocopy" ):
        os.environ["EMERGE_NOCOPY"] = str( True )
    elif ( i == "--noclean" ):
        os.environ["EMERGE_NOCLEAN"] = str( True )
    elif ( i == "--clean" ):
        os.environ["EMERGE_NOCLEAN"] = str( False )
    elif ( i in [ "--version-dir", "--version-package", "--print-installable",
                  "--print-installed", "--print-targets" ] ):
        buildAction = i[2:]
        stayQuiet = True
        if i in [ "--print-installable", "--print-installed" ]:
            break
    elif ( i == "-i" ):
        ignoreInstalled = True
    elif ( i == "--update" ):
        ignoreInstalled = True
        os.environ["EMERGE_NOCLEAN"] = str( True )
    elif ( i == "--update-all" ):
        ignoreInstalled = True
        os.environ["EMERGE_NOCLEAN"] = str( True )
        updateAll = True
    elif ( i == "--install-deps" ):
        ignoreInstalled = True
        buildAction = "install-deps"
    elif ( i in [ "--fetch", "--unpack", "--preconfigure", "--configure", "--compile", "--make",
                  "--install", "--qmerge", "--manifest", "--package", "--unmerge", "--test",
                  "--full-package" ] ):
        buildAction = i[2:]
    elif ( i.startswith( "-" ) ):
        usage()
        exit ( 1 )
    else:
        packageName = i
        break

nextArguments = sys.argv[ (sys.argv.index( i ) + 1): ]

if stayQuiet == True:
    verbose = 0
    os.environ["EMERGE_VERBOSE"] = str( verbose )

# get KDEROOT from env
KDEROOT = os.getenv( "KDEROOT" )

utils.debug( "buildAction: %s" % buildAction )
utils.debug( "doPretend: %s" % doPretend )
utils.debug( "packageName: %s" % packageName )
utils.debug( "buildType: %s" % os.getenv( "EMERGE_BUILDTYPE" ) )
utils.debug( "buildTests: %s" % os.getenv( "EMERGE_BUILDTESTS" ) )
utils.debug( "verbose: %s" % os.getenv( "EMERGE_VERBOSE" ) )
utils.debug( "KDEROOT: %s\n" % KDEROOT )
utils.debug_line()

def unset_var( varname ):
    if not os.getenv( varname ) == None:
        print
        utils.warning( "%s found as environment variable. you cannot override emerge"\
                       " with this - unsetting %s locally" % ( varname, varname ) )
        os.environ[ varname ]=""

unset_var( "CMAKE_INCLUDE_PATH" )
unset_var( "CMAKE_LIBRARY_PATH" )
unset_var( "CMAKE_FIND_PREFIX" )
unset_var( "CMAKE_INSTALL_PREFIX" )

# adding emerge/bin to find base.py and gnuwin32.py etc.
os.environ["PYTHONPATH"] = os.getenv( "PYTHONPATH" ) + ";" +\
                           os.path.join( os.getcwd(), os.path.dirname( executableName ) )
sys.path.append( os.path.join( os.getcwd(), os.path.dirname( executableName ) ) )

deplist = []
packageList = []
categoryList = []

if packageName:
    if len( packageName.split( "/" ) ) == 1:
        if utils.isCategory( packageName ):
            utils.debug( "isCategory=True", 2 )
            packageList = utils.getAllPackages( packageName )
            categoryList = [ packageName ]
        else:
            if utils.getCategory( packageName ):
                packageList = [ packageName ]
                categoryList = [ utils.getCategory( packageName ) ]
            else:
                utils.warning( "unknown category or package: %s" % packageName )
    elif len( packageName.split( "/" ) ) == 2:
        [ cat, pac ] = packageName.split( "/" )
        validPackage = False
        if utils.isCategory( cat ):
            categoryList = [ cat ]
        else:
            utils.warning( "unknown category %s; ignoring package %s" % ( cat, packageName ) )
        if len( categoryList ) > 0 and utils.isPackage( categoryList[0], pac ):
            packageList = [ pac ]
        if len( categoryList ) and len( packageList ):
            utils.debug( "added package %s/%s" % ( categoryList[0], pac ), 2 )
        else:
            utils.debug( "ignoring package %s" % packageName )
    else:
        utils.error( "unknown packageName" )
elif updateAll:
    installedPackages = utils.getInstallables()
    utils.debug( "Updating, no package spec given", 1 )
    packageList = []
    for category, package, version in installedPackages:
        if utils.isInstalled( category, package, version ) and utils.isPackageUpdateable( category, package, version ):
            categoryList.append( category )
            packageList.append( package )
    utils.debug( "Will update packages: " + str (packageList), 1 )

for entry in packageList:
    utils.debug( "%s" % entry, 1 )
utils.debug_line( 1 )

for category, entry in zip (categoryList, packageList):
    utils.solveDependencies( category, entry, "", deplist )

for item in range( len( deplist ) ):
    if deplist[ item ][ 0 ] in categoryList and deplist[ item ][ 1 ] in packageList:
        deplist[ item ].append( ignoreInstalled )
    else:
        deplist[ item ].append( False )

    utils.debug( "dependency: %s" % deplist[ item ], 1 )

for item in deplist:
    cat = item[ 0 ]
    pac = item[ 1 ]
    ver = item[ 2 ]

    if utils.isInstalled( cat, pac, ver ) and updateAll and not utils.isPackageUpdateable( cat, pac, ver ):
        print "remove:", cat, pac, ver
        deplist.remove( item )

if buildAction == "install-deps":
    # the first dependency is the package itself - ignore it
    # TODO: why are we our own dependency?
    del deplist[ 0 ]

deplist.reverse()
success = True
# package[0] -> category
# package[1] -> package
# package[2] -> version

if ( buildAction != "all" and buildAction != "install-deps" ):
    """ if a buildAction is given, then do not try to build dependencies
        and do the action although the package might already be installed.
        This is still a bit problematic since packageName might not be a valid
        package"""
        
    if packageName and len(deplist) >= 1:
        package = deplist[ -1 ]
    else:
        package = [ None, None, None ]
    ok = handlePackage( package[ 0 ], package[ 1 ], package[ 2 ], buildAction, opts )
else:
    for package in deplist:
        if ( utils.isInstalled( package[0], package[1], package[2] ) and not package[ -1 ] ):
            if utils.verbose() > 1 and package[1] == packageName:
                utils.warning( "already installed %s/%s-%s" % ( package[0], package[1], package[2] ) )
            elif utils.verbose() > 2 and not package[1] == packageName:
                utils.warning( "already installed %s/%s-%s" % ( package[0], package[1], package[2] ) )
        else:
            instver = utils.findInstalled( package[0], package[1] )
            if ( doPretend ):
                if utils.verbose() > 0:
                    utils.warning( "pretending %s/%s-%s" % ( package[0], package[1], package[2] ) )
            else:
                if( instver != None ):
                    utils.debug( "found old version %s - removing" % instver )
                    handlePackage( package[0], package[1], package[2], "unmerge", opts )

                action = buildAction
                if buildAction == "install-deps":
                  action = "all"
                if not handlePackage( package[0], package[1], package[2], action, opts ):
                    utils.error( "fatal error: package %s/%s-%s %s failed" % \
                        (package[0], package[1], package[2], buildAction) )
                    exit( 1 )

print                        
if len( nextArguments ) > 0:
    command = "\"" + sys.executable + "\" -u " + executableName + " " + " ".join( nextArguments )

    for element in environ.keys():
        if environ[ element ]:
            os.environ[ element ] = environ[ element ]
        elif element == "EMERGE_VERBOSE":
            os.environ[ element ] = "1"
        else:
            os.environ[ element ] = ""
    utils.system( command ) or utils.die( "cannot execute next commands cmd: %s" % command )
