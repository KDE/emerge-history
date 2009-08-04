# -*- coding: utf-8 -*-

import info;
import utils;
import portage;
import os;
import sys;
import datetime;

## @todo complete a release and binary merge dir below rootdir 
# 1.  enable build type related merge install settings
# 2a. use different install databases for debug and release
# 3. binary packages which are build type independent should be 
# marked in both databases or should have a separate install database
# question: How to detect reliable this case ? 


ROOTDIR=os.getenv( "KDEROOT" )
COMPILER=os.getenv( "KDECOMPILER" )
DOWNLOADDIR=os.getenv( "DOWNLOADDIR" )
if ( DOWNLOADDIR == None ):
    DOWNLOADDIR=os.path.join( ROOTDIR, "distfiles" )

KDESVNDIR=os.getenv( "KDESVNDIR" )
if ( KDESVNDIR == None ):
    KDESVNDIR=os.path.join( DOWNLOADDIR, "svn-src", "kde" )
KDESVNSERVER=os.getenv( "KDESVNSERVER" )
if ( KDESVNSERVER == None ):
    KDESVNSERVER="svn://anonsvn.kde.org"
KDESVNUSERNAME=os.getenv( "KDESVNUSERNAME" )
KDESVNPASSWORD=os.getenv( "KDESVNPASSWORD" )

# ok, we have the following dirs:
# ROOTDIR: the root where all this is below
# DOWNLOADDIR: the dir under rootdir, where the downloaded files are put into
# WORKDIR: the directory, under which the files are unpacked and compiled.
#            here rootdir/tmp/packagename/work
# IMAGEDIR: the directory, under which the compiled files are installed.
#            here rootdir/tmp/packagename/image


class EmergeBase():
    """base class for emerge system - holds attributes and methods required by base classes"""
    
    def __init__( self, SRC_URI="", **args ):
        utils.debug( "EmergeBase.__init__ called", 2 )
        if hasattr(self,'alreadyCalled'):
            return
        self.alreadyCalled = True
        self.buildTarget = None

        if "args" in args.keys() and "env" in args["args"].keys():
            env = args["args"]["env"]
        else:
            env = dict( os.environ )
            
        if "args" in args.keys() and "argv0" in args["args"].keys():
            self.argv0 = args["args"]["argv0"]
        else:
            self.argv0 = sys.argv[ 0 ]
            
        self.SRC_URI                = SRC_URI
        self.noCopy                 = False
        self.noClean                = False
        self.noFast                 = True
        self.buildTests             = False
        self.forced                 = False
        self.versioned              = False
        self.noFetch                = False
        self.CustomDefines       = ""
        self.createCombinedPackage  = False
     
        ## specifies if a build type related root directory should be used
        if os.getenv("EMERGE_MERGE_ROOT_WITH_BUILD_TYPE") <> None:
            self.useBuildTypeRelatedMergeRoot = os.getenv("EMERGE_MERGE_ROOT_WITH_BUILD_TYPE")
        else:
            self.useBuildTypeRelatedMergeRoot = False
        
        self.isoDateToday           = str( datetime.date.today() ).replace('-', '')

        self.setDirectoriesBase()
        #self.msys = msys_build.msys_interface()
        #self.kde  = KDE4BuildSystem()
        
        if os.getenv( "EMERGE_OFFLINE" ) == "True":
            self.noFetch = True
        if os.getenv( "EMERGE_NOCOPY" ) == "True":
            self.noCopy = True
        if os.getenv( "EMERGE_NOFAST" ) == "False":
            self.noFast = False
        if os.getenv( "EMERGE_NOCLEAN" )    == "True":
            self.noClean     = True
        if os.getenv( "EMERGE_FORCED" ) == "True":
            self.forced = True
        if os.getenv( "EMERGE_BUILDTESTS" ) == "True":
            self.buildTests = True

        if COMPILER == "msvc2005":
            self.__compiler = "msvc2005"
        elif COMPILER == "msvc2008":
            self.__compiler = "msvc2008"
        elif COMPILER == "mingw":
            self.__compiler = "mingw"
        elif COMPILER == "mingw4":
            self.__compiler = "mingw4"
        else:
            print >> sys.stderr, "emerge error: KDECOMPILER: %s not understood" % COMPILER
            exit( 1 )

    def abstract():
        import inspect
        caller = inspect.getouterframes(inspect.currentframe())[1][3]
        raise NotImplementedError(caller + ' must be implemented in subclass')

    def buildType(self):
        """return currently selected build type"""
        Type=os.getenv( "EMERGE_BUILDTYPE" )
        if ( not Type == None ):
            buildType = Type
        else:
            buildType = None
        return buildType

    def compiler(self):
        """return currently selected compiler"""
        return self.__compiler

    def downloadDir(self): 
        """ location of directory where fetched files are  stored """
        return DOWNLOADDIR
        
    def packageDir(self): 
        """ add documentation """
        return os.path.join( portage.rootDir(), self.category, self.package )
    
    def filesDir(self):
        """ add documentation """
        return os.path.join( self.packageDir(), "files" )
        
    def buildRoot(self):
        """return absolute path to the root directory of the currently active package"""
        buildroot    = os.path.join( ROOTDIR, "build", self.category, self.PV )
        return buildroot

    def workDir(self):
        """return absolute path to the 'work' subdirectory of the currently active package"""
        _workDir = os.path.join( self.buildRoot(), "work" )
        return _workDir

    def buildDir(self):        
        utils.debug("EmergeBase.buildDir() called" ,2)
        if( self.buildType() == None ):
            tmp = "%s-%s-%s" % (COMPILER, "default", self.buildTarget)
        else:
            tmp = "%s-%s-%s" % (COMPILER, self.buildType(), self.buildTarget)
        
        ## \todo for what is this good ?
        #if( not self.buildNameExt == None ):
        #    tmp = "%s-%s" % (COMPILER, self.buildNameExt)

        builddir = os.path.join( self.workDir(), tmp )
                
        utils.debug("package builddir is: %s" % builddir,2)
        return builddir

    def imageDir(self):
        """return absolute path to the install root directory of the currently active package
        """
        imagedir = os.path.join( self.buildRoot(), "image" )

        # we assume that binary packages are for all compiler and targets
        ## \todo add image dir support for using binary packages for a specific compiler and build type
        if hasattr(self, 'buildSystemType') and self.buildSystemType == 'binary':
            return imagedir
        
        imagedir += '-' + COMPILER
        imagedir += '-' + self.buildType()
        imagedir += '-' + self.buildTarget
        
        return imagedir

    def installDir(self):
        """return absolute path to the install directory of the currently active package. 
        This path may point to a subdir of imageDir() in case @ref info.targetInstallPath is used 
        """
        if self.subinfo.hasInstallPath():
            installDir = os.path.join( self.imageDir(), self.subinfo.installPath())
        else:
            installDir = self.imageDir()
        return installDir

    def mergeSourceDir(self):
        """return absolute path to the merge source directory of the currently active package. 
        This path may point to a subdir of imageDir() in case @ref info.targetInstallPath is used 
        """
        if self.subinfo.hasMergeSourcePath():
            installDir = os.path.join( self.imageDir(), self.subinfo.mergeSourcePath())
        else:
            installDir = self.imageDir()
        return installDir
                        
    def mergeDestinationDir(self):
        """return absolute path to the merge directory of the currently active package. 
        This path may point to a subdir of rootdir in case @ref info.targetMergePath is used 
        """            

        if self.subinfo.hasMergePath():
            dir = os.path.join(ROOTDIR, self.subinfo.mergePath())
        elif not self.useBuildTypeRelatedMergeRoot:
            dir = ROOTDIR
        elif self.buildType() == 'Debug':
            dir = os.path.join(ROOTDIR,'debug')
        elif self.buildType() == 'Release':
            dir = os.path.join(ROOTDIR,'release')
        else:
            dir = ROOTDIR
        return dir

    def setBuildTarget( self, target = None):
        self.subinfo.setBuildTarget(target)
        self.buildTarget = self.subinfo.buildTarget
        if hasattr(self,'source'):
            self.source.buildTarget = self.subinfo.buildTarget
        
    def setup( self, fileName, category, package, version ):
        """ called from internal instance creating """
        self.rootdir = ROOTDIR
        self.category = category
        self.package = package
        self.version = version
        ( self.PV, ext ) = os.path.splitext( os.path.basename( fileName) )
        self.setBuildTarget()

    ## \todo cleanup 
    def setDirectoriesBase( self ):
        """setting all important stuff that isn't coped with in the c'tor"""
        """parts will probably go to infoclass"""
        utils.debug( "setdirectories called", 2 )

        ( self.PV, ext ) = os.path.splitext( os.path.basename( self.argv0 ) )

        ( self.category, self.package, self.version ) = \
                       portage.getCategoryPackageVersion( self.argv0 )

        utils.debug( "setdir category: %s, package: %s" % ( self.category, self.package ), 1 )

        self.rootdir     = ROOTDIR

    def enterBuildDir(self):
       
        if ( not os.path.exists( self.buildDir()) ):
            os.makedirs( self.buildDir() )
            if utils.verbose() > 0:
                print "creating: %s" % self.buildDir()

        os.chdir( self.buildDir() )
        if utils.verbose() > 0:
            print "entering: %s" % self.buildDir()

